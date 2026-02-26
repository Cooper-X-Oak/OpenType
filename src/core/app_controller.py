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
from src.utils.logger import logger
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
        
        # UI
        self.tray = SystemTray()
        self.settings_window = SettingsWindow()
        self.cursor_indicator = CursorIndicator()
        
        # Core
        self.recorder = None
        self.reload_recorder()
        
        self.stt_engine = STTEngine(self.config.get("api_key"))
        self.hotkey_manager = HotkeyManager()
        self.text_injector = TextInjector()
        
        self.is_processing = False
        self.processing_lock = threading.Lock()
        
        # Connect Signals
        self.connect_signals()
        
        # Register Hotkey
        self.update_hotkey()
        
    def connect_signals(self):
        # UI Signals
        self.tray.settings_requested.connect(self.open_settings)
        self.tray.exit_requested.connect(self.quit_app)
        self.settings_window.settings_saved.connect(self.on_settings_saved)
        
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
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.error_occurred.emit(str(e))

    def stop_and_process(self):
        # Called from HotkeyManager thread
        try:
            self.recorder.stop()
            self.recording_stopped.emit()
            
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
        self.tray.showMessage("OpenType Error", message, QSystemTrayIcon.Warning, 3000)
