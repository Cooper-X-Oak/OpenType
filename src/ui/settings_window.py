from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
import pyaudio
from src.core.config_manager import config_manager
from src.utils.logger import logger

class SettingsWindow(QWidget):
    settings_saved = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenType Settings")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint) # Optional

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-...")
        self.api_key_input.setText(config_manager.get("api_key", ""))
        self.form_layout.addRow("DashScope API Key:", self.api_key_input)

        # Hotkey
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("e.g. f2, ctrl+alt+v")
        self.hotkey_input.setText(config_manager.get("hotkey", "f2"))
        self.form_layout.addRow("Global Hotkey:", self.hotkey_input)

        # Audio Device
        self.device_combo = QComboBox()
        self.devices = self.get_audio_devices()
        self.device_combo.addItems([d['name'] for d in self.devices])
        
        current_device_index = config_manager.get("audio_device_index")
        if current_device_index is not None:
            # Find index in our list (which might filter devices)
            # Actually PyAudio index is unique.
            # Let's map PyAudio index to combo box index.
            for i, device in enumerate(self.devices):
                if device['index'] == current_device_index:
                    self.device_combo.setCurrentIndex(i)
                    break
        
        self.form_layout.addRow("Microphone:", self.device_combo)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.button_layout)

    def get_audio_devices(self):
        p = pyaudio.PyAudio()
        devices = []
        try:
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    name = p.get_device_info_by_host_api_device_index(0, i).get('name')
                    devices.append({'index': i, 'name': name})
        except Exception as e:
            logger.error(f"Error listing audio devices: {e}")
        finally:
            p.terminate()
        return devices

    def save_settings(self):
        api_key = self.api_key_input.text().strip()
        hotkey = self.hotkey_input.text().strip()
        
        # Get selected device index
        device_idx = self.device_combo.currentIndex()
        if device_idx >= 0 and device_idx < len(self.devices):
            audio_device_index = self.devices[device_idx]['index']
        else:
            audio_device_index = None

        if not api_key:
            QMessageBox.warning(self, "Warning", "API Key is required for STT.")
            # We allow saving empty key but warn
        
        if not hotkey:
            QMessageBox.warning(self, "Error", "Hotkey cannot be empty.")
            return

        config_manager.set("api_key", api_key)
        config_manager.set("hotkey", hotkey)
        config_manager.set("audio_device_index", audio_device_index)
        
        logger.info("Settings saved.")
        self.settings_saved.emit()
        self.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
