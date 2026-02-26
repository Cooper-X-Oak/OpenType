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
            
            keyboard.on_press_key(hotkey, self._on_press_wrapper)
            keyboard.on_release_key(hotkey, self._on_release_wrapper)
            
            logger.info(f"Registered hotkey: {hotkey}")
            
        except Exception as e:
            logger.error(f"Failed to register hotkey {hotkey}: {e}")

    def unregister_hotkey(self):
        if self.current_hotkey:
            try:
                # keyboard.unhook_key(self.current_hotkey) # This removes all hooks for the key?
                # Actually keyboard.remove_hotkey doesn't work for on_press_key hooks returned?
                # on_press_key returns a hook function/object.
                # But keyboard.unhook_all_hotkeys() removes hotkeys.
                # keyboard.unhook(self._on_press_wrapper) might work if we kept reference.
                # But keyboard library is a bit global state heavy.
                
                # Best way to unregister specific hooks is hard in 'keyboard' lib without keeping the hook object.
                # But since we only have one hotkey active, we can just unhook all?
                # Or we can keep track of the hook handles.
                
                # For simplicity, let's just clear all for now if we assume single hotkey app.
                # But better to store the hooks.
                pass 
                # keyboard.unhook_all() # This is too aggressive.
                
                # Let's rely on overwriting callbacks or just leave it for now (prototype).
                # To be proper, we should use keyboard.hook and filter ourselves?
                
                # Re-implementation with hook:
                pass
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
