from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QSystemTrayIcon
from src.core.config_manager import config_manager
from src.core.audio_recorder import AudioRecorder
from src.core.audio_processor import normalize_audio
from src.core.stt_engine import STTEngine
from src.core.hotkey_manager import HotkeyManager
from src.core.text_injector import TextInjector
from src.ui.system_tray import SystemTray
from src.ui.settings_window import SettingsWindow
from src.ui.cursor_indicator import CursorIndicator
from src.ui.onboarding_window import GeekOnboardingWindow
from src.utils.logger import logger
from src.utils.sound_player import play_start_sound, play_stop_sound, play_error_sound
import threading

class AppController(QObject):
    recording_started = Signal()
    recording_stopped = Signal()
    processing_finished = Signal(str) # Emits recognized text or error
    error_occurred = Signal(str)

    def __init__(self, app):
        super().__init__()
        self.app = app
        
        # Initialize components
        self.config = config_manager
        self.onboarding = None
        
        # UI
        self.tray = SystemTray()
        self.settings_window = SettingsWindow()
        self.cursor_indicator = CursorIndicator()
        
        # Connect UI Signals early
        self.tray.settings_requested.connect(self.open_settings)
        self.tray.geek_mode_requested.connect(self.start_onboarding)
        self.tray.exit_requested.connect(self.quit_app)
        self.settings_window.settings_saved.connect(self.on_settings_saved)
        
        # Check for first run or missing/invalid key
        # Condition:
        # 1. No API key configured
        # 2. Key is clearly invalid (e.g. "your_key_here" or empty)
        # 3. Explicit "force_onboarding" flag in config
        
        api_key = self.config.get("api_key")
        is_key_invalid = not api_key or api_key.strip() == "" or "your_key" in api_key.lower()
        
        if is_key_invalid or self.config.get("force_onboarding"):
             logger.info("Starting Onboarding: Missing or invalid API key, or forced.")
             self.start_onboarding()
        else:
             logger.info("Starting Silently: Valid configuration found.")
             self.init_core_features()

    def start_onboarding(self):
        logger.info("Starting onboarding requested")
        if self.onboarding:
            logger.info("Onboarding window exists, showing and activating")
            if self.onboarding.isMinimized():
                self.onboarding.showNormal()
            self.onboarding.show()
            self.onboarding.raise_()
            self.onboarding.activateWindow()
            return

        current_config = {
            "api_key": self.config.get("api_key", ""),
            "hotkey": self.config.get("hotkey", "alt+space"),
            "sound_enabled": self.config.get("sound_enabled", True)
        }
        self.onboarding = GeekOnboardingWindow(initial_config=current_config)
        self.onboarding.finished.connect(self.on_onboarding_finished)
        # Handle manual close to allow reopening
        self.onboarding.destroyed.connect(self._reset_onboarding_ref)
        self.onboarding.show()

    def _reset_onboarding_ref(self):
        logger.info("Onboarding window destroyed, resetting reference")
        self.onboarding = None

    def on_onboarding_finished(self, config_data):
        logger.info("Onboarding finished, saving config and initializing core")
        # Save config
        for key, value in config_data.items():
            self.config.set(key, value)
        
        # Initialize core
        self.init_core_features()
        if self.onboarding:
            self.onboarding.close()
            self.onboarding = None

    def init_core_features(self):
        # Core
        self.recorder = None
        self.reload_recorder()
        
        self.stt_engine = STTEngine(self.config.get("api_key"))
        self.hotkey_manager = HotkeyManager()
        self.text_injector = TextInjector()
        
        self.is_processing = False
        self.processing_lock = threading.Lock()
        
        # Connect Core Signals
        self.connect_core_signals()
        
        # Register Hotkey
        self.update_hotkey()
        
    def connect_core_signals(self):
        # App Signals (for UI updates)
        self.recording_started.connect(self.tray.set_recording_icon)
        self.recording_started.connect(self.cursor_indicator.show)
        self.recording_stopped.connect(self.tray.set_idle_icon)
        self.recording_stopped.connect(self.cursor_indicator.hide)
        self.processing_finished.connect(self.on_processing_finished)
        self.error_occurred.connect(self.show_error) # Notification

    def reload_recorder(self):
        if self.recorder:
            try:
                self.recorder.close()
            except Exception as e:
                logger.error(f"Error closing recorder: {e}")
        
        device_index = self.config.get("audio_device_index")
        self.recorder = AudioRecorder(device_index=device_index)
        # Connect audio level signal
        self.recorder.audio_level_changed.connect(self.cursor_indicator.set_level)
        logger.info(f"AudioRecorder reloaded with device index: {device_index}")

    def update_hotkey(self):
        hotkey = self.config.get("hotkey")
        if hotkey:
            self.hotkey_manager.register_hotkey(
                hotkey, 
                self.start_recording, 
                self.stop_and_process
            )

    def start_recording(self):
        # Called from HotkeyManager thread
        with self.processing_lock:
            if self.is_processing:
                logger.warning("Already processing, ignoring press.")
                return

        try:
            self.recorder.start()
            self.recording_started.emit()
            play_start_sound()
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.error_occurred.emit(str(e))

    def stop_and_process(self):
        # Called from HotkeyManager thread
        try:
            # Idempotency check: if not recording, don't stop/process again
            if not self.recorder or not self.recorder.recording:
                logger.warning("Stop requested but not recording. Ignoring.")
                return

            self.recorder.stop()
            self.recording_stopped.emit()
            play_stop_sound()
            
            # Start processing in background (it is already in a thread from HotkeyManager)
            # But HotkeyManager spawns a thread for callback.
            # So we are in a worker thread.
            self.process_audio()
            
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            self.error_occurred.emit(str(e))

    def process_audio(self):
        with self.processing_lock:
            self.is_processing = True
        
        try:
            audio_data = self.recorder.get_audio_data()
            if not audio_data or len(audio_data) < 1000: # Ignore very short clicks
                logger.warning("Audio too short or empty, ignoring.")
                # Silenced: self.tray.showMessage("OpenType", "Recording too short.", QSystemTrayIcon.Warning, 2000)
                return

            # Normalize
            target_db = self.config.get("target_dbfs", -20.0)
            
            # Calculate RMS for debugging
            import numpy as np
            samples = np.frombuffer(audio_data, dtype=np.int16)
            rms = np.sqrt(np.mean(samples**2))
            logger.info(f"Captured audio: {len(audio_data)} bytes, RMS: {rms:.2f}")
            
            if rms < 20: # Lowered threshold
                logger.warning(f"Audio seems silent (RMS < 20). RMS: {rms:.2f}")
                # self.tray.showMessage("OpenType Warning", "Microphone seems silent.", QSystemTrayIcon.Warning, 3000)
            
            normalized_data = normalize_audio(audio_data, target_db)
            
            # STT
            # Update API key in case it changed
            self.stt_engine.set_api_key(self.config.get("api_key"))
            text, error = self.stt_engine.recognize(normalized_data)
            
            if text:
                logger.info(f"Recognized: {text}")
                # Inject
                self.text_injector.inject_text(text)
                self.processing_finished.emit(text)
            else:
                if error:
                    logger.error(f"STT Error: {error}")
                    self.error_occurred.emit(f"STT Error: {error}")
                else:
                    logger.warning("STT returned empty text.")
                    # Silenced: self.tray.showMessage("OpenType", "No speech detected.", QSystemTrayIcon.Warning, 2000)
                
        except Exception as e:
            logger.error(f"Processing error: {e}")
            self.error_occurred.emit(str(e))
        finally:
            with self.processing_lock:
                self.is_processing = False

    def open_settings(self):
        self.settings_window.show()
        self.settings_window.activateWindow()

    def on_settings_saved(self):
        # Reload hotkey
        self.update_hotkey()
        # Reload recorder
        self.reload_recorder()

    def quit_app(self):
        self.tray.hide()
        self.hotkey_manager.clear()
        self.app.quit()

    def on_processing_finished(self, text):
        # Silenced success notification to avoid interruption
        # self.tray.showMessage("OpenType", f"Input: {text}", QSystemTrayIcon.Information, 2000)
        pass

    def show_error(self, message):
        play_error_sound()
        self.tray.showMessage("OpenType Error", message, QSystemTrayIcon.Warning, 3000)
