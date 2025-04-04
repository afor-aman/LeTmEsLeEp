#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal

from automation import KeyboardAutomation


class KeyboardTab(QWidget):
    """Tab for keyboard automation settings and control."""
    
    # Signal for status updates
    status_update = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize automation
        self.automation = KeyboardAutomation()
        self.automation.status_update.connect(self.status_update)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Interval settings group
        interval_group = QGroupBox("Typing Interval (seconds)")
        interval_layout = QFormLayout()
        
        # Min interval input
        self.min_interval_spin = QDoubleSpinBox()
        self.min_interval_spin.setRange(0.01, 1.0)
        self.min_interval_spin.setSingleStep(0.01)
        self.min_interval_spin.setValue(self.automation.min_interval)
        interval_layout.addRow("Minimum Interval:", self.min_interval_spin)
        
        # Max interval input
        self.max_interval_spin = QDoubleSpinBox()
        self.max_interval_spin.setRange(0.01, 1.0)
        self.max_interval_spin.setSingleStep(0.01)
        self.max_interval_spin.setValue(self.automation.max_interval)
        interval_layout.addRow("Maximum Interval:", self.max_interval_spin)
        
        # Randomize checkbox
        self.randomize_check = QCheckBox("Randomize Typing Speed")
        self.randomize_check.setChecked(self.automation.randomize_typing)
        interval_layout.addRow("", self.randomize_check)
        
        interval_group.setLayout(interval_layout)
        main_layout.addWidget(interval_group)
        
        # Text input group
        text_group = QGroupBox("Text to Type")
        text_layout = QVBoxLayout()
        
        # Text input
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter text to type...")
        self.text_edit.setText(self.automation.text_to_type)
        
        text_layout.addWidget(self.text_edit)
        text_group.setLayout(text_layout)
        main_layout.addWidget(text_group)
        
        # Add stretch to push all controls to the top
        main_layout.addStretch(1)
        
        # Connect signals
        self.min_interval_spin.valueChanged.connect(self._update_settings)
        self.max_interval_spin.valueChanged.connect(self._update_settings)
        self.randomize_check.stateChanged.connect(self._update_settings)
        self.text_edit.textChanged.connect(self._update_text)
    
    def _update_settings(self):
        """Update automation settings based on UI inputs."""
        # Update min interval
        self.automation.min_interval = self.min_interval_spin.value()
        
        # Update max interval (ensure it's >= min interval)
        if self.max_interval_spin.value() < self.automation.min_interval:
            self.max_interval_spin.setValue(self.automation.min_interval)
        self.automation.max_interval = self.max_interval_spin.value()
        
        # Update randomize setting
        self.automation.randomize_typing = self.randomize_check.isChecked()
        
        # Emit status update
        self.status_update.emit("Keyboard settings updated")
    
    def _update_text(self):
        """Update text to type."""
        self.automation.text_to_type = self.text_edit.toPlainText()
    
    def start_automation(self):
        """Start the keyboard automation."""
        self._update_settings()
        self._update_text()
        
        # Check if text is empty
        if not self.automation.text_to_type:
            self.status_update.emit("Error: No text to type")
            return False
        
        self.automation.start()
        return True
    
    def stop_automation(self):
        """Stop the keyboard automation."""
        self.automation.stop()
    
    def pause_automation(self):
        """Pause the keyboard automation."""
        self.automation.pause()
    
    def resume_automation(self):
        """Resume the keyboard automation."""
        self.automation.resume()
    
    def reset_settings(self):
        """Reset settings to default values."""
        # Reset to default values
        self.min_interval_spin.setValue(0.1)
        self.max_interval_spin.setValue(0.3)
        self.randomize_check.setChecked(True)
        self.text_edit.setText("The quick brown fox jumps over the lazy dog.")
        
        # Update settings
        self._update_settings()
        self._update_text() 