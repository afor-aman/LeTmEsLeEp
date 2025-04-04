#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QCheckBox, QComboBox, QPushButton, 
    QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QSettings


class SettingsDialog(QDialog):
    """Dialog for global application settings."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup dialog properties
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        # Initialize settings
        self.settings = QSettings("LetMeSleep", "AutomationTool")
        
        # Initialize UI
        self._init_ui()
        
        # Load settings
        self._load_settings()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # General settings group
        general_group = QGroupBox("General Settings")
        general_layout = QFormLayout()
        
        # Start minimized option
        self.start_minimized_check = QCheckBox("Start application minimized")
        general_layout.addRow("", self.start_minimized_check)
        
        # Safety timeout option
        self.safety_timeout_check = QCheckBox("Enable safety timeout (30 min)")
        general_layout.addRow("", self.safety_timeout_check)
        
        general_group.setLayout(general_layout)
        main_layout.addWidget(general_group)
        
        # Theme settings group
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QFormLayout()
        
        # Default theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_layout.addRow("Default Theme:", self.theme_combo)
        
        theme_group.setLayout(theme_layout)
        main_layout.addWidget(theme_group)
        
        # Safety settings group
        safety_group = QGroupBox("Safety Settings")
        safety_layout = QFormLayout()
        
        # Confirmation dialogs option
        self.confirm_dialogs_check = QCheckBox("Show confirmation dialogs")
        safety_layout.addRow("", self.confirm_dialogs_check)
        
        # Cursor safety area option
        self.cursor_safety_check = QCheckBox("Enable cursor safety area (10px border)")
        safety_layout.addRow("", self.cursor_safety_check)
        
        safety_group.setLayout(safety_layout)
        main_layout.addWidget(safety_group)
        
        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self._apply_settings)
        
        main_layout.addWidget(button_box)
    
    def _load_settings(self):
        """Load settings from QSettings."""
        # Load general settings
        self.start_minimized_check.setChecked(
            self.settings.value("general/start_minimized", False, type=bool)
        )
        self.safety_timeout_check.setChecked(
            self.settings.value("general/safety_timeout", True, type=bool)
        )
        
        # Load theme settings
        theme_index = 1 if self.settings.value("theme/default", "dark") == "dark" else 0
        self.theme_combo.setCurrentIndex(theme_index)
        
        # Load safety settings
        self.confirm_dialogs_check.setChecked(
            self.settings.value("safety/confirm_dialogs", True, type=bool)
        )
        self.cursor_safety_check.setChecked(
            self.settings.value("safety/cursor_safety", True, type=bool)
        )
    
    def _save_settings(self):
        """Save settings to QSettings."""
        # Save general settings
        self.settings.setValue(
            "general/start_minimized", 
            self.start_minimized_check.isChecked()
        )
        self.settings.setValue(
            "general/safety_timeout", 
            self.safety_timeout_check.isChecked()
        )
        
        # Save theme settings
        theme = "dark" if self.theme_combo.currentIndex() == 1 else "light"
        self.settings.setValue("theme/default", theme)
        
        # Save safety settings
        self.settings.setValue(
            "safety/confirm_dialogs", 
            self.confirm_dialogs_check.isChecked()
        )
        self.settings.setValue(
            "safety/cursor_safety", 
            self.cursor_safety_check.isChecked()
        )
        
        # Sync settings
        self.settings.sync()
    
    def _apply_settings(self):
        """Apply the current settings."""
        self._save_settings()
    
    def accept(self):
        """Handle dialog acceptance."""
        self._save_settings()
        super().accept() 