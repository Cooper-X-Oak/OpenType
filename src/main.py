import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.core.app_controller import AppController
from src.utils.logger import logger

def main():
    # Allow only one instance? (Optional, use QLockFile or similar)
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep running for tray icon
    
    try:
        controller = AppController(app)
        logger.info("OpenType started.")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
