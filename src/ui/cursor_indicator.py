from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QCursor
from src.utils.logger import logger

class CursorIndicator(QWidget):
    def __init__(self):
        super().__init__()
        # Frameless, Always on top, Tool (no taskbar entry), Transparent
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool | 
            Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Geometry
        self.base_size = 60
        self.resize(self.base_size, self.base_size)
        
        # State
        self.level = 0.0
        self.target_level = 0.0
        
        # Timer for position and smooth animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_state)
        # 60 FPS
        self.timer.start(16)
        
        self.hide()
        
    def update_state(self):
        if not self.isVisible():
            return
            
        # Follow cursor
        cursor_pos = QCursor.pos()
        # Follow cursor center (negative offset to center on cursor tip)
        # Center of widget (30,30) aligns with cursor (0,0) -> offset (-30,-30)
        # But we want it slightly offset to not cover the exact click point
        # Try aligning top-left of widget to top-left of cursor with slight negative offset
        self.move(cursor_pos.x() - 10, cursor_pos.y() - 10)
        
        # Smooth level interpolation
        # Easing: move 20% towards target per frame
        self.level += (self.target_level - self.level) * 0.2
        
        # Always update if visible to keep position in sync, 
        # but repaint logic is handled by paintEvent
        self.update()
            
    def set_level(self, level):
        # Scale level for better visual dynamic range
        # Input is 0.0-1.0
        self.target_level = max(0.0, min(1.0, level))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.rect().center()
        
        # Dynamic Radius based on level
        # Min radius 8, Max radius 25
        base_radius = 8
        dynamic_radius = base_radius + (self.level * 15)
        
        # 1. Outer Glow (The "Wave")
        # Alpha decreases as size increases
        alpha = int(100 + (self.level * 100)) # 100-200
        color = QColor(0, 120, 215, alpha)
        
        # If very loud, turn slightly orange/red
        if self.level > 0.7:
            # Interpolate towards red
            ratio = (self.level - 0.7) / 0.3
            color = QColor(
                int(0 + 255 * ratio), 
                int(120 - 120 * ratio), 
                int(215 - 100 * ratio), 
                alpha
            )
            
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, dynamic_radius, dynamic_radius)
        
        # 2. Inner Core (Solid Dot)
        # Always visible so user knows it's there even when silent
        painter.setBrush(QBrush(QColor(255, 255, 255, 220)))
        painter.drawEllipse(center, 4, 4)
