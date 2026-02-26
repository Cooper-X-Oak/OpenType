from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PySide6.QtCore import Signal, Qt
from src.utils.logger import logger
from src.core.version import __version__

class SystemTray(QSystemTrayIcon):
    settings_requested = Signal()
    geek_mode_requested = Signal()
    exit_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip(f"OpenType v{__version__} - Typeless Input")
        
        # Load icon (placeholder)
        # We can use standard icons from QStyle if available, 
        # but QSystemTrayIcon needs QIcon.
        # Let's try to load from resources if exists, else use a default or empty.
        # QIcon.fromTheme("audio-input-microphone") might work on Linux, Windows depends.
        # We can create a simple QPixmap and set it.
        
        self.menu = QMenu(parent)
        
        self.geek_action = QAction("Open Geek Console", self)
        self.geek_action.triggered.connect(self.geek_mode_requested.emit)
        self.menu.addAction(self.geek_action)
        
        self.settings_action = QAction("Classic Settings", self)
        self.settings_action.triggered.connect(self.settings_requested.emit)
        self.menu.addAction(self.settings_action)
        
        self.menu.addSeparator()
        
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(self.exit_action)
        
        self.setContextMenu(self.menu)
        
        # Handle activation (e.g. double click)
        self.activated.connect(self.on_activated)
        
        # Set default icon
        self.set_idle_icon()
        
        self.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger: # Single click
            pass 
        elif reason == QSystemTrayIcon.DoubleClick:
            logger.info("Tray Double Clicked")
            self.geek_mode_requested.emit()

    def set_idle_icon(self):
        # Create a simple icon programmatically if no file
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor("gray"))
        painter.drawEllipse(4, 4, 24, 24)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.setToolTip("OpenType: Idle")

    def set_recording_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor("red"))
        painter.drawEllipse(4, 4, 24, 24)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.setToolTip("OpenType: Recording...")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    import sys
    
    app = QApplication(sys.argv)
    # App needs to keep running
    app.setQuitOnLastWindowClosed(False)
    
    tray = SystemTray()
    
    sys.exit(app.exec())
