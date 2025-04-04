#!/usr/bin/env python3
import sys
import os
import logging
import traceback
import qdarktheme
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

# Handle bundled application resources
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    except Exception:
        return relative_path

# Configure logging
log_dir = os.path.join(os.path.expanduser("~"), ".letmesleep")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "letmesleep.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LetMeSleep")

# Global exception handler
def global_exception_handler(exctype, value, tb):
    """Handle uncaught exceptions."""
    # Log the exception
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    logger.error("Uncaught exception: {}".format(error_msg))
    
    # Show error dialog
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Unhandled Error")
    msg_box.setText("An unhandled error occurred:")
    msg_box.setInformativeText(str(value))
    msg_box.setDetailedText(error_msg)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
    
    # Call the default exception handler
    sys.__excepthook__(exctype, value, tb)

def main():
    try:
        # Set global exception handler
        sys.excepthook = global_exception_handler
        
        # Start the application
        app = QApplication(sys.argv)
        
        # Apply dark theme by default
        app.setPalette(qdarktheme.load_palette("dark"))
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
        
        # Set application icon
        icon_path = resource_path("resources/icons/bot.svg")
        app.setWindowIcon(QIcon(icon_path))
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        # Start event loop
        return app.exec_()
    except Exception as e:
        logger.critical("Failed to start application: {}".format(str(e)))
        traceback.print_exc()
        
        # If QApplication is not created yet, show console error
        if 'app' not in locals() or not app.instance():
            print("CRITICAL ERROR: {}".format(str(e)))
            return 1
            
        # Otherwise show error dialog
        QMessageBox.critical(
            None, 
            "Startup Error",
            "Failed to start application: {}".format(str(e)),
            QMessageBox.Ok
        )
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 