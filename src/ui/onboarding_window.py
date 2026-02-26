import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QApplication, QFrame, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Signal, QTimer
from src.core.audio_recorder import AudioRecorder
from src.utils.logger import logger

class GeekOnboardingWindow(QWidget):
    finished = Signal(dict)  # Emits config dict when done

    def __init__(self, initial_config=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Dragging logic
        self._dragging = False
        self._drag_start_pos = None

        # Data
        self.config_data = {
            "api_key": "",
            "hotkey": "alt+space",
            "sound_enabled": True
        }
        self.input_mode = "" # Initialize input mode

        if initial_config:
            self.config_data.update(initial_config)
            
        self.step = 0
        self.steps = [
            self.step_welcome,
            self.step_hotkey,
            self.step_mic_test,
            self.step_api_key,
            self.step_finish
        ]

        # UI Setup
        self.resize(600, 350)
        self.center_window()
        self.setup_ui()
        
        self.recorder = None
        
        # Start
        QTimer.singleShot(500, self.next_step)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            event.accept()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # --- UI Components ---
    
    def _create_label(self, text, style_key):
        lbl = QLabel(text)
        if style_key == "title":
            lbl.setStyleSheet("color: #666666; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 12px;")
        elif style_key == "display":
            lbl.setStyleSheet("color: #D4D4D4; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 16px; line-height: 1.5;")
        elif style_key == "hint":
            lbl.setStyleSheet("color: #666666; font-size: 14px;")
        elif style_key == "nav_btn":
            lbl.setStyleSheet("QLabel { color: #666666; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 14px; padding: 4px 8px; } QLabel:hover { color: #FFFFFF; background-color: #333333; border-radius: 4px; }")
        return lbl

    def setup_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container (The "Terminal" Window)
        self.container = QFrame()
        self.container.setObjectName("TerminalContainer")
        self.container.setStyleSheet("#TerminalContainer { background-color: #1E1E1E; border: 1px solid #333333; border-radius: 8px; }")
        self.main_layout.addWidget(self.container)
        
        # Content Layout
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)

        # 1. Header
        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self._create_label("[ SYSTEM INIT ]", "title"))
        self.header_layout.addStretch()
        
        # Window Controls
        for text, callback, hover_color in [("[-]", self.showMinimized, "#D4D4D4"), ("[x]", self.close, "#FF5555")]:
            btn = QLabel(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"QLabel {{ color: #666666; font-family: 'Consolas'; font-size: 14px; padding: 2px 5px; }} QLabel:hover {{ color: {hover_color}; background-color: #333333; border-radius: 3px; }}")
            btn.mousePressEvent = lambda e, cb=callback: cb()
            self.header_layout.addWidget(btn)
        self.content_layout.addLayout(self.header_layout)

        # 1.5 Progress Indicator
        self.progress_layout = QHBoxLayout()
        self.progress_layout.setSpacing(15)
        self.progress_layout.setContentsMargins(0, 0, 0, 10)
        self.progress_labels = []
        for name in ["INIT", "HOTKEY", "MIC", "CLOUD", "READY"]:
            lbl = QLabel(name)
            lbl.setStyleSheet("color: #333333; font-family: 'Consolas'; font-size: 12px;")
            self.progress_layout.addWidget(lbl)
            self.progress_labels.append(lbl)
        self.progress_layout.addStretch()
        self.content_layout.addLayout(self.progress_layout)

        # 2. Main Display
        self.display_label = self._create_label("", "display")
        self.display_label.setWordWrap(True)
        self.content_layout.addWidget(self.display_label)
        
        # 3. Interactive Menu Area
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(0, 10, 0, 0)
        self.content_layout.addWidget(self.menu_container)
        self.menu_container.hide()

        # 5. Mic Test Container
        self.mic_container = QWidget()
        self.mic_layout = QVBoxLayout(self.mic_container)
        self.mic_level_bar = QLabel("[..............................] 0%")
        self.mic_level_bar.setAlignment(Qt.AlignCenter)
        self.mic_level_bar.setStyleSheet("color: #00FF00; font-family: 'Consolas'; font-size: 24px; font-weight: bold;")
        self.mic_layout.addWidget(self.mic_level_bar)
        self.mic_layout.addWidget(self._create_label("请尝试说话... 看到音量跳动后按 [Enter] 继续", "hint"))
        self.content_layout.addWidget(self.mic_container)
        self.mic_container.hide()

        # 6. Input Area
        self.input_container = QWidget()
        self.input_layout = QHBoxLayout(self.input_container)
        prompt = QLabel(">")
        prompt.setStyleSheet("color: #007ACC; font-family: 'Consolas'; font-size: 18px; font-weight: bold;")
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background: transparent; border: none; color: #FFFFFF; font-family: 'Consolas'; font-size: 18px;")
        self.input_field.returnPressed.connect(self.handle_input)
        self.input_layout.addWidget(prompt)
        self.input_layout.addWidget(self.input_field)
        self.content_layout.addWidget(self.input_container)
        self.input_container.hide()

        # 5. Footer (Navigation) - Removed per user request for simplification
        self.content_layout.addStretch()

    def type_text(self, text, callback=None):
        self.display_label.setText("")
        self.full_text = text
        self.char_index = 0
        self.type_callback = callback
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self._type_char)
        self.type_timer.start(5) # Typing speed (faster)

    def _type_char(self):
        # Type multiple chars at once to be faster
        chunk_size = 3
        if self.char_index < len(self.full_text):
            end_index = min(self.char_index + chunk_size, len(self.full_text))
            self.display_label.setText(self.full_text[:end_index] + "█")
            self.char_index = end_index
        else:
            self.type_timer.stop()
            self.display_label.setText(self.full_text) # Remove cursor
            if self.type_callback:
                self.type_callback()

    def next_step(self):
        self.update_progress()
        if self.step < len(self.steps):
            self.steps[self.step]()
        else:
            self.close()
            self.finished.emit(self.config_data)

    def update_progress(self):
        for i, lbl in enumerate(self.progress_labels):
            if i == self.step:
                # Active
                lbl.setText(f"[ {lbl.text().replace('[', '').replace(']', '').strip()} ]")
                lbl.setStyleSheet("color: #00FF00; font-weight: bold; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 14px;")
            elif i < self.step:
                # Completed
                lbl.setText(f"{lbl.text().replace('[', '').replace(']', '').strip()}")
                lbl.setStyleSheet("color: #666666; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 12px;")
            else:
                # Pending
                lbl.setText(f"{lbl.text().replace('[', '').replace(']', '').strip()}")
                lbl.setStyleSheet("color: #333333; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 12px;")

    def jump_to_step(self, index):
        if index == self.step:
            return
        
        # Cleanup current
        self.cleanup_current_step()
        
        # Jump
        self.step = index
        self.next_step()

    # --- Steps ---

    def step_welcome(self):
        msg = "正在初始化 OPENTYPE 核心模块...\n\n加载模块:\n[OK] 音频捕获 (Audio Capture)\n[OK] 热键管理 (Hotkey Manager)\n[OK] 界面渲染 (UI Renderer)\n\n系统就绪。\n按 [Enter] 继续，或点击上方导航切换。"
        self.type_text(msg, self.enable_welcome_interaction)

    def enable_welcome_interaction(self):
        self.input_mode = "welcome"
        self.setFocus()

    def step_api_key(self):
        current_key = self.config_data.get("api_key", "")
        # Check if it looks like a valid key (not empty, maybe check prefix if standard)
        if current_key and len(current_key) > 5:
            masked = current_key[:3] + "*" * 6 + current_key[-4:]
            msg = f"云端服务配置。\n\n检测到已有 API Key: {masked}\n\n[Enter] 继续使用，或输入新 Key 覆盖。"
            self.type_text(msg, self.show_input_prefilled)
        else:
            msg = "最后一步: 云端服务。\n\n请输入 DashScope API Key 以启用语音识别。\n\n(提示: 可直接按 [Enter] 跳过，稍后在配置文件中设置)"
            self.type_text(msg, self.show_input)
        
        self.input_mode = "api_key"

    def show_input_prefilled(self):
        self.show_input()
        # Set placeholder to indicate current value is kept if empty
        self.input_field.setPlaceholderText("按 Enter 保持当前 Key")

    def step_hotkey(self):
        msg = "配置: 激活热键。\n请选择一种触发方式 (推荐使用非组合单键):"
        self.type_text(msg, self.show_hotkey_menu)
        self.input_mode = "hotkey_menu"

    def step_mic_test(self):
        msg = "硬件检测: 麦克风灵敏度。\n请对着麦克风说话..."
        self.type_text(msg, self.start_mic_test)

    def start_mic_test(self):
        self.input_mode = "mic_test"
        self.mic_container.show()
        self.setFocus()
        
        try:
            if not self.recorder:
                self.recorder = AudioRecorder()
                self.recorder.audio_level_changed.connect(self.update_mic_level)
            self.recorder.start()
        except Exception as e:
            logger.error(f"Failed to start mic test: {e}")
            self.mic_level_bar.setText("麦克风启动失败")
            self.mic_level_bar.setStyleSheet("color: #FF5555; font-size: 18px;")
            self.mic_hint.setText(f"错误: {str(e)}\n按 [Enter] 跳过")

    def update_mic_level(self, level):
        # level is 0.0 to 1.0 (approx)
        width = 30
        val = min(1.0, max(0.0, level))
        filled = int(val * width)
        bar = "█" * filled + "░" * (width - filled)
        percent = int(val * 100)
        
        # Dynamic color based on level
        if val > 0.8:
            color = "#FF5555" # Red
        elif val > 0.5:
            color = "#FFFF55" # Yellow
        else:
            color = "#00FF00" # Green
            
        self.mic_level_bar.setText(f"[{bar}] {percent}%")
        self.mic_level_bar.setStyleSheet(f"color: {color}; font-family: 'Consolas', 'Microsoft YaHei'; font-size: 24px; font-weight: bold;")

    def stop_mic_test(self):
        if self.recorder:
            try:
                self.recorder.stop()
                self.recorder.close() # Close to release resource
                self.recorder = None
            except Exception as e:
                logger.error(f"Error stopping mic test: {e}")
        self.mic_container.hide()

    def step_finish(self):
        # Hide menu if visible
        if hasattr(self, 'menu_container'):
            self.menu_container.hide()
        if hasattr(self, 'mic_container'):
            self.mic_container.hide()
            
        self.input_container.hide()
        hotkey_display = self.config_data.get("hotkey", "未知").upper()
        msg = f"配置已保存。\n\nOPENTYPE 已在后台运行。\n按下 [ {hotkey_display} ] 开始录音。\n\n享受编程的乐趣吧。"
        self.type_text(msg, self.finish_sequence)

    def finish_sequence(self):
        QTimer.singleShot(1000, self.next_step)

    # --- Interaction Handlers ---

    def show_input(self):
        self.input_container.show()
        self.input_field.setEchoMode(QLineEdit.Normal)
        self.input_field.setText("")
        self.input_field.setFocus()

    def show_hotkey_menu(self):
        # Clear previous if any
        if hasattr(self, 'menu_container'):
            self.menu_container.deleteLater()
            
        self.menu_container = QWidget()
        menu_layout = QVBoxLayout(self.menu_container)
        menu_layout.setSpacing(5)
        
        # Define options with full text
        self.hotkey_options = [
            {"id": "1", "text": "Right Alt (推荐)", "val": "right alt"},
            {"id": "2", "text": "F2", "val": "f2"},
            {"id": "3", "text": "Left Alt", "val": "left alt"}
        ]
        
        self.menu_items = []
        for i, opt in enumerate(self.hotkey_options):
            btn = QPushButton(opt["text"])
            btn.setProperty("opt_val", opt["val"])
            btn.setProperty("opt_index", i)
            btn.setProperty("opt_text", opt["text"])
            
            # Simple Click Handler
            btn.clicked.connect(lambda checked=False, v=opt["val"]: self.select_menu_option(v))
            
            # Cursor
            btn.setCursor(Qt.PointingHandCursor)
            
            menu_layout.addWidget(btn)
            self.menu_items.append(btn)
            
        self.content_layout.addWidget(self.menu_container)
        self.menu_container.show()
        
        # Select first by default
        self.current_menu_index = 0
        self.update_menu_selection()
        
        # Focus for key navigation
        self.setFocus()

    def update_menu_selection(self):
        for i, btn in enumerate(self.menu_items):
            if i == self.current_menu_index:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #00FF00; 
                        font-family: 'Consolas', 'Microsoft YaHei'; 
                        font-size: 16px; 
                        font-weight: bold;
                        background-color: #333333;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        text-align: left;
                    }
                """)
                btn.setText(f"> [ {btn.property('opt_text')} ]")
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #AAAAAA; 
                        font-family: 'Consolas', 'Microsoft YaHei'; 
                        font-size: 14px;
                        background-color: transparent;
                        border: none;
                        padding: 8px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        color: #FFFFFF;
                        background-color: #2D2D2D;
                    }
                """)
                btn.setText(f"  [ {btn.property('opt_text')} ]")

    def select_menu_option(self, val):
        self.config_data["hotkey"] = val
        self.cleanup_current_step()
        self.step += 1
        self.next_step()

    def handle_input(self):
        # Only used for API Key input now
        text = self.input_field.text().strip()
        
        if self.input_mode == "api_key":
            if text:
                self.config_data["api_key"] = text
            else:
                # If text is empty, check if we had a key before
                pass 
                
            # Always proceed, even if empty (skip or keep)
            self.input_container.hide()
            self.input_field.clear() 
            self.input_field.setPlaceholderText("") # Reset placeholder
            self.next_step()

    def cleanup_current_step(self):
        """Reset UI state before switching steps"""
        # Hide all possible containers
        if hasattr(self, 'menu_container'): self.menu_container.hide()
        if hasattr(self, 'mic_container'): self.mic_container.hide()
        if hasattr(self, 'capture_container'): self.capture_container.hide()
        if hasattr(self, 'input_container'): self.input_container.hide()
        
        # Stop mic test if running
        if self.input_mode == "mic_test":
            self.stop_mic_test()

    def keyPressEvent(self, event):
        key = event.key()

        # Global Navigation
        # 1. Backspace -> Previous Step
        if key == Qt.Key_Backspace:
            should_go_back = True
            # Only block backspace if we are typing in API key field
            if self.input_mode == "api_key" and self.input_field.hasFocus():
                if self.input_field.text(): # If has text, let it delete
                    should_go_back = False
            
            if should_go_back and self.step > 0:
                self.cleanup_current_step()
                self.step -= 1
                self.next_step()
                event.accept()
                return

        # 2. Enter -> Next Step / Confirm
        if key in (Qt.Key_Return, Qt.Key_Enter):
            if self.input_mode == "hotkey_menu":
                # Special handling for menu selection
                if 0 <= self.current_menu_index < len(self.menu_items):
                    self.select_menu_option(self.menu_items[self.current_menu_index].property("opt_val"))
                event.accept()
                return
            else:
                # Default: Go Next
                self.cleanup_current_step()
                self.step += 1
                self.next_step()
                event.accept()
                return

        # Mode Specific Handling (Arrows, Escape)
        if self.input_mode == "hotkey_menu":
            if key == Qt.Key_Up:
                self.current_menu_index = max(0, self.current_menu_index - 1)
                self.update_menu_selection()
                event.accept()
            elif key == Qt.Key_Down:
                self.current_menu_index = min(len(self.menu_items) - 1, self.current_menu_index + 1)
                self.update_menu_selection()
                event.accept()

        elif self.input_mode == "mic_test":
             if key == Qt.Key_Escape:
                 self.stop_mic_test()
                 event.accept()
             
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeekOnboardingWindow()
    window.show()
    sys.exit(app.exec())
