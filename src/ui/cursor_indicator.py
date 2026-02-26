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
        
        # Geometry for "Capsule & EKG" style
        # Fixed size vertical capsule
        self.capsule_width = 14
        self.capsule_height = 32
        self.resize(self.capsule_width + 4, self.capsule_height + 4) # Small padding
        
        # State
        self.level = 0.0
        self.target_level = 0.0
        
        # Import random for EKG noise
        import random
        self.random = random

        
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
        # For new capsule (14x32), center it vertically on the cursor tip?
        # Or slightly below?
        # Let's keep it to the right, centered vertically on the text line.
        self.move(cursor_pos.x() + 10, cursor_pos.y() - 10)
        
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
        center_y = rect.height() / 2
        
        # --- 1. Draw Container (Capsule) ---
        # Fixed size centered
        w = self.capsule_width
        h = self.capsule_height
        
        # Black background, 90% opacity
        bg_color = QColor(0, 0, 0, 230)
        # White thin border
        border_color = QColor(255, 255, 255, 200)
        
        capsule_rect = QRectF(center_x - w/2, center_y - h/2, w, h)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, 1))
        # Fully rounded corners (capsule shape)
        painter.drawRoundedRect(capsule_rect, w/2, w/2)
        
        # --- 2. Draw Voice Waveform (EKG/Oscilloscope) ---
        # Cyberpunk Neon Green
        wave_color = QColor(0, 255, 65) # Neon Green
        painter.setPen(QPen(wave_color, 1.5))
        painter.setBrush(Qt.NoBrush)
        
        # Wave parameters
        # Height of the wave area (keep some padding inside capsule)
        wave_h = h - 8 
        wave_top = center_y - wave_h/2
        
        # Generate points
        # 6 segments (7 points)
        points = []
        num_points = 7
        segment_h = wave_h / (num_points - 1)
        
        # Max amplitude (horizontal swing)
        # Max swing is +/- (w/2 - 2px padding)
        # Increase amplitude range to allow going slightly outside the capsule for visual impact?
        # Let's keep it mostly inside but maximize usage.
        max_amp = (w/2) + 2 # Allow slight overflow for intense effect
        
        for i in range(num_points):
            y = wave_top + (i * segment_h)
            
            # Anchor top and bottom points to center
            if i == 0 or i == num_points - 1:
                x = center_x
            else:
                # Random noise + amplitude based on level
                # Base jitter even at silence (alive feel)
                jitter = self.random.uniform(-0.5, 0.5)
                
                # Boost signal intensity
                # Use non-linear response (power) to make loud sounds more dramatic
                boosted_level = pow(self.level, 0.7) 
                
                # Signal swing
                signal = self.random.uniform(-1.0, 1.0) * boosted_level * max_amp
                
                x = center_x + jitter + signal
                
            points.append( (x, y) )
            
        # Draw Polyline
        from PySide6.QtCore import QPointF
        qpoints = [QPointF(x, y) for x, y in points]
        painter.drawPolyline(qpoints)
