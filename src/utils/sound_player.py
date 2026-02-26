import winsound
import threading
from src.utils.logger import logger

def _play_beep_async(freq, duration):
    try:
        winsound.Beep(freq, duration)
    except Exception as e:
        logger.error(f"Failed to play beep: {e}")

def play_start_sound():
    """Play a short high-pitched beep to indicate recording start."""
    threading.Thread(target=_play_beep_async, args=(800, 150), daemon=True).start()

def play_stop_sound():
    """Play a short lower-pitched beep to indicate recording stop/processing."""
    threading.Thread(target=_play_beep_async, args=(400, 150), daemon=True).start()

def play_error_sound():
    """Play a system error sound."""
    def _play_system_sound():
        try:
            winsound.MessageBeep(winsound.MB_ICONHAND)
        except Exception as e:
            logger.error(f"Failed to play error sound: {e}")
            
    threading.Thread(target=_play_system_sound, daemon=True).start()
