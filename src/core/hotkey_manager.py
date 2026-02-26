import keyboard
import threading
from src.utils.logger import logger

class HotkeyManager:
    def __init__(self):
        self.current_hotkey = None
        self.is_pressed = False
        self.press_callback = None
        self.release_callback = None
        self.lock = threading.Lock()
        self.hooks = []

    def register_hotkey(self, hotkey, on_press, on_release):
        """
        Register a hotkey with press and release callbacks.
        Only supports single key hotkeys well for hold-to-speak (e.g. 'f2', 'alt', 'ctrl').
        Complex combinations might be tricky with hold detection.
        """
        if self.current_hotkey:
            self.unregister_hotkey()

        self.current_hotkey = hotkey
        self.press_callback = on_press
        self.release_callback = on_release
        self.is_pressed = False
        
        try:
            # We use hook_key to detect press and release of the specific key
            # keyboard.on_press_key(hotkey, self._on_key_event)
            # keyboard.on_release_key(hotkey, self._on_key_event)
            
            # Note: on_press_key/on_release_key adds a hook that is called for every event of that key.
            # We need to filter repeats.
            
            press_hook = keyboard.on_press_key(hotkey, self._on_press_wrapper)
            release_hook = keyboard.on_release_key(hotkey, self._on_release_wrapper)
            self.hooks.append(press_hook)
            self.hooks.append(release_hook)
            
            logger.info(f"Registered hotkey: {hotkey}")
            
        except Exception as e:
            logger.error(f"Failed to register hotkey {hotkey}: {e}")

    def unregister_hotkey(self):
        if self.current_hotkey:
            try:
                for hook in self.hooks:
                    keyboard.unhook(hook)
                self.hooks.clear()
            except Exception as e:
                logger.error(f"Failed to unregister hotkey: {e}")
            
            self.current_hotkey = None

    def _on_press_wrapper(self, event):
        with self.lock:
            if not self.is_pressed:
                self.is_pressed = True
                if self.press_callback:
                    # Run callback in a separate thread to avoid blocking the hook
                    threading.Thread(target=self.press_callback, daemon=True).start()

    def _on_release_wrapper(self, event):
        with self.lock:
            if self.is_pressed:
                self.is_pressed = False
                if self.release_callback:
                    threading.Thread(target=self.release_callback, daemon=True).start()

    def clear(self):
        keyboard.unhook_all()

if __name__ == "__main__":
    # Test
    import time
    
    def pressed():
        print("Pressed!")
        
    def released():
        print("Released!")
        
    manager = HotkeyManager()
    print("Press F2 to test (Hold it)...")
    manager.register_hotkey('f2', pressed, released)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.clear()
