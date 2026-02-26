from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QCursor, QPen
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
        
        # Geometry for "Terminal Block" style
        # Tall and narrow
        self.base_width = 12
        self.base_height = 30 
        self.resize(self.base_width + 10, self.base_height + 10) # Add padding for glow
        
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
        
        # New Position Logic for "Terminal Block"
        # Ideally, sit to the right of the cursor, like a text caret.
        # Cursor tip is usually top-left.
        # Let's position it slightly to the right and centered vertically relative to a line of text.
        # Assuming cursor is at bottom-left of a character (standard text cursor),
        # but mouse cursor tip is top-left.
        # Let's try placing it:
        # X: cursor.x + 15 (right of pointer)
        # Y: cursor.y - 10 (centered on pointer tip vertically)
        
        # User requested: "Don't take up space".
        # Maybe keep it close: x + 8, y - 10
        self.move(cursor_pos.x() + 8, cursor_pos.y() - 10)
        
        # Smooth level interpolation
        # Easing: move 20% towards target per frame
        self.level += (self.target_level - self.level) * 0.2
        
        self.update()
            
    def set_level(self, level):
        # Scale level for better visual dynamic range
        # Input is 0.0-1.0
        self.target_level = max(0.0, min(1.0, level))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Center of the widget rect
        rect = self.rect()
        center_x = rect.width() / 2
        bottom_y = rect.height() - 5 # 5px padding from bottom
        
        # Style: Terminal Block
        # Base state: A thin underscore (height ~3px)
        # Active state: Grows upwards to full block (height ~20px)
        
        min_h = 3
        max_h = 24
        current_h = min_h + (self.level * (max_h - min_h))
        
        # Width fixed
        w = 8
        
        # Draw "Glow" / Shadow first (for visibility on white)
        # A slightly larger, semi-transparent black rect behind
        glow_rect = QRectF(center_x - w/2 - 1, bottom_y - current_h - 1, w + 2, current_h + 2)
        painter.setBrush(QBrush(QColor(0, 0, 0, 50))) # Faint shadow
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(glow_rect, 1, 1)
        
        # Draw Main Block
        # Color: Terminal Green
        # Dynamic alpha: slightly transparent at low volume, solid at high
        alpha = int(180 + (self.level * 75)) # 180-255
        color = QColor(0, 255, 0, alpha)
        
        # If very loud, turn slightly yellow/amber (warning)
        if self.level > 0.8:
            # Interpolate towards amber
            ratio = (self.level - 0.8) / 0.2
            color = QColor(
                int(0 + 255 * ratio), 
                255, 
                0, 
                alpha
            )

        block_rect = QRectF(center_x - w/2, bottom_y - current_h, w, current_h)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(block_rect, 1, 1) # Slight rounded corners
