import pyperclip
import keyboard
import time
import threading
from src.utils.logger import logger

class TextInjector:
    def __init__(self):
        self.lock = threading.Lock()

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
                # Store old clipboard content if needed? (Optional, maybe later)
                # old_clipboard = pyperclip.paste()
                
                pyperclip.copy(text)
                logger.info(f"Copied to clipboard: {text[:20]}...")
                
                # 2. Simulate Ctrl+V
                # Add a small delay to ensure clipboard is ready?
                time.sleep(0.1)
                
                # Send Ctrl+V
                keyboard.send('ctrl+v')
                logger.info("Sent Ctrl+V")
                
                # Restore clipboard? (Optional)
                # time.sleep(0.1)
                # pyperclip.copy(old_clipboard)
                
            except Exception as e:
                logger.error(f"Failed to inject text: {e}")

if __name__ == "__main__":
    # Test
    injector = TextInjector()
    print("Injecting 'Hello World' in 3 seconds...")
    time.sleep(3)
    injector.inject_text("Hello World")
