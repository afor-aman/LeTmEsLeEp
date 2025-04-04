#!/usr/bin/env python3
import sys
import os
import qdarktheme
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QComboBox, QTabWidget,
    QStatusBar, QMessageBox, QAction, QToolBar, QApplication
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.combined_panel import CombinedPanel
from ui.settings_dialog import SettingsDialog
from ui.help_dialog import HelpDialog

# Handle bundled application resources
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    except Exception:
        return relative_path

class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("LetMeSleep - Automation Tool")
        self.setWindowIcon(QIcon(resource_path("resources/icons/bot.svg")))
        self.setMinimumSize(800, 600)  # Increased height to accommodate new controls
        
        # Initialize UI components
        self._init_ui()
        
        # Set up status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Setup theme 
        self.current_theme = "dark"
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tool bar
        self._create_toolbar()
        
        # Create combined panel
        self.combined_panel = CombinedPanel()
        self.combined_panel.status_update.connect(self._update_status)
        self.combined_panel.failsafe_triggered.connect(self._handle_failsafe)
        self.combined_panel.error_occurred.connect(self._handle_error)
        
        # Add combined panel to main layout
        main_layout.addWidget(self.combined_panel)
        
        # Create control buttons
        control_layout = QHBoxLayout()
        
        # Start/Stop button
        self.start_stop_button = QPushButton("Start Both")
        self.start_stop_button.setMinimumWidth(120)
        self.start_stop_button.clicked.connect(self._start_stop)
        
        # Pause/Resume button
        self.pause_resume_button = QPushButton("Pause Both")
        self.pause_resume_button.setMinimumWidth(120)
        self.pause_resume_button.setEnabled(False)
        self.pause_resume_button.clicked.connect(self._pause_resume)
        
        # Reset button
        self.reset_button = QPushButton("Reset All")
        self.reset_button.setMinimumWidth(120)
        self.reset_button.clicked.connect(self._reset)
        
        # Exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setMinimumWidth(120)
        self.exit_button.clicked.connect(self.close)
        
        # Add buttons to control layout
        control_layout.addWidget(self.start_stop_button)
        control_layout.addWidget(self.pause_resume_button)
        control_layout.addWidget(self.reset_button)
        control_layout.addWidget(self.exit_button)
        
        # Add control layout to main layout
        main_layout.addLayout(control_layout)
    
    def _create_toolbar(self):
        """Create the toolbar with actions."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)
        toolbar.addAction(settings_action)
        
        # Help action
        help_action = QAction("Help", self)
        help_action.triggered.connect(self._show_help)
        toolbar.addAction(help_action)
        
        # Theme action
        self.theme_action = QAction("Switch to Light Theme", self)
        self.theme_action.triggered.connect(self._toggle_theme)
        toolbar.addAction(self.theme_action)
    
    def _handle_failsafe(self):
        """Handle failsafe trigger event."""
        self.start_stop_button.setText("Start Both")
        self.pause_resume_button.setText("Pause Both")
        self.pause_resume_button.setEnabled(False)
        self.status_bar.showMessage("FAILSAFE TRIGGERED! All automations stopped", 5000)  # Show for 5 seconds
        
        # Show failsafe message box
        QMessageBox.warning(
            self, "Failsafe Triggered",
            "The failsafe has been triggered by moving the mouse to the screen corner.\n\n"
            "All automations have been stopped for your safety.",
            QMessageBox.Ok
        )
    
    def _start_stop(self):
        """Handle start/stop button click."""
        if self.start_stop_button.text() == "Start Both":
            # Start both automations
            if self.combined_panel.start_automation():
                self.start_stop_button.setText("Stop Both")
                self.pause_resume_button.setEnabled(True)
                self.status_bar.showMessage("All automations started")
        else:
            # Stop all automations
            self.combined_panel.stop_automation()
            self.start_stop_button.setText("Start Both")
            self.pause_resume_button.setText("Pause Both")
            self.pause_resume_button.setEnabled(False)
            self.status_bar.showMessage("All automations stopped")
    
    def _pause_resume(self):
        """Handle pause/resume button click."""
        if self.pause_resume_button.text() == "Pause Both":
            # Pause all automations
            self.combined_panel.pause_automation()
            self.pause_resume_button.setText("Resume Both")
            self.status_bar.showMessage("All automations paused")
        else:
            # Resume all automations
            self.combined_panel.resume_automation()
            self.pause_resume_button.setText("Pause Both")
            self.status_bar.showMessage("All automations resumed")
    
    def _reset(self):
        """Reset all automation settings."""
        self.combined_panel.reset_settings()
        self.status_bar.showMessage("All settings reset to default")
    
    def _show_settings(self):
        """Show the settings dialog."""
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
    
    def _show_help(self):
        """Show the help dialog."""
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == "dark":
            QApplication.instance().setPalette(qdarktheme.load_palette("light"))
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet("light"))
            self.current_theme = "light"
            self.theme_action.setText("Switch to Dark Theme")
        else:
            QApplication.instance().setPalette(qdarktheme.load_palette("dark"))
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet("dark"))
            self.current_theme = "dark" 
            self.theme_action.setText("Switch to Light Theme")
    
    def _update_status(self, message):
        """Update the status bar with a message."""
        self.status_bar.showMessage(message)
    
    def _handle_error(self, message):
        """Handle error occurred event."""
        # Show error in status bar
        self.status_bar.showMessage(f"ERROR: {message}", 5000)  # Show for 5 seconds
        
        # If automation is running, stop it on critical errors
        if "maximum error retries exceeded" in message.lower() or "fatal" in message.lower():
            self.combined_panel.stop_automation()
            self.start_stop_button.setText("Start Both")
            self.pause_resume_button.setText("Pause Both")
            self.pause_resume_button.setEnabled(False)
            
            # Show error dialog for critical errors
            QMessageBox.critical(
                self, "Automation Error",
                f"The automation has been stopped due to a critical error:\n\n{message}\n\n"
                f"Please check the application logs for more details.",
                QMessageBox.Ok
            )
        # For non-critical errors, just log and continue
        else:
            # Log to console
            print(f"ERROR: {message}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 'Exit Confirmation',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Stop any running automation
            self.combined_panel.stop_automation()
            event.accept()
        else:
            event.ignore() 