import pyperclip
import keyboard
import time
import threading
import ctypes
from ctypes import wintypes
from src.utils.logger import logger

class TextInjector:
    def __init__(self):
        self.lock = threading.Lock()

    def _send_ctrl_v_ctypes(self):
        """
        Simulate Ctrl+V using low-level Windows API (SendInput).
        This is more robust than keyboard module in some packaged environments.
        """
        VK_CONTROL = 0x11
        VK_V = 0x56
        KEYEVENTF_KEYUP = 0x0002
        INPUT_KEYBOARD = 1

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [("wVk", wintypes.WORD),
                        ("wScan", wintypes.WORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", ctypes.c_ulong)]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", wintypes.DWORD),
                        ("ki", KEYBDINPUT),
                        ("pad", ctypes.c_ubyte * 8)]

        def create_input(vk, flags):
            ki = KEYBDINPUT(vk, 0, flags, 0, 0)
            return INPUT(INPUT_KEYBOARD, ki, (ctypes.c_ubyte * 8)())

        # Split inputs to ensure target app registers the key combination
        # 1. Ctrl Down
        input_ctrl_down = create_input(VK_CONTROL, 0)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_ctrl_down), cbSize)
        time.sleep(0.05)
        
        # 2. V Down
        input_v_down = create_input(VK_V, 0)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_v_down), cbSize)
        time.sleep(0.05)
        
        # 3. V Up
        input_v_up = create_input(VK_V, KEYEVENTF_KEYUP)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_v_up), cbSize)
        time.sleep(0.05)
        
        # 4. Ctrl Up
        input_ctrl_up = create_input(VK_CONTROL, KEYEVENTF_KEYUP)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_ctrl_up), cbSize)

    def inject_text(self, text):
        """
        Inject text into the currently active window by simulating Ctrl+V.
        """
        if not text:
            logger.warning("No text to inject.")
            return

        with self.lock:
            try:
                # 1. Copy text to clipboard
                pyperclip.copy(text)
                logger.info(f"Copied to clipboard: {text[:20]}...")
                
                # 2. Simulate Ctrl+V
                time.sleep(0.3) # Increased wait time for clipboard to stabilize
                
                # Try ctypes method first (more reliable on Windows)
                try:
                    self._send_ctrl_v_ctypes()
                    logger.info("Sent Ctrl+V (via ctypes)")
                except Exception as e:
                    logger.warning(f"ctypes injection failed, falling back to keyboard module: {e}")
                    keyboard.send('ctrl+v')
                    logger.info("Sent Ctrl+V (via keyboard)")
                
            except Exception as e:
                logger.error(f"Failed to inject text: {e}")

if __name__ == "__main__":
    # Test
    injector = TextInjector()
    print("Injecting 'Hello World' in 3 seconds...")
    time.sleep(3)
    injector.inject_text("Hello World")
