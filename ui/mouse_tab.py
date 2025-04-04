#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QRadioButton, QSlider, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal

from automation import MouseAutomation


class MouseTab(QWidget):
    """Tab for mouse automation settings and control."""
    
    # Signal for status updates
    status_update = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize automation
        self.automation = MouseAutomation()
        self.automation.status_update.connect(self.status_update)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Interval settings group
        interval_group = QGroupBox("Movement Interval (seconds)")
        interval_layout = QFormLayout()
        
        # Min interval input
        self.min_interval_spin = QDoubleSpinBox()
        self.min_interval_spin.setRange(0.1, 10.0)
        self.min_interval_spin.setSingleStep(0.1)
        self.min_interval_spin.setValue(self.automation.min_interval)
        interval_layout.addRow("Minimum Interval:", self.min_interval_spin)
        
        # Max interval input
        self.max_interval_spin = QDoubleSpinBox()
        self.max_interval_spin.setRange(0.1, 10.0)
        self.max_interval_spin.setSingleStep(0.1)
        self.max_interval_spin.setValue(self.automation.max_interval)
        interval_layout.addRow("Maximum Interval:", self.max_interval_spin)
        
        interval_group.setLayout(interval_layout)
        main_layout.addWidget(interval_group)
        
        # Movement path group
        path_group = QGroupBox("Movement Path")
        path_layout = QVBoxLayout()
        
        # Path selection
        self.path_combo = QComboBox()
        self.path_combo.addItems(["Straight", "ZigZag", "Random"])
        # Set current path based on automation settings
        path_index = {
            "straight": 0,
            "zigzag": 1,
            "random": 2
        }.get(self.automation.movement_path, 2)
        self.path_combo.setCurrentIndex(path_index)
        
        path_layout.addWidget(self.path_combo)
        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)
        
        # Click type group
        click_group = QGroupBox("Click Type")
        click_layout = QVBoxLayout()
        
        # Click type selection
        self.click_combo = QComboBox()
        self.click_combo.addItems(["None", "Left Click", "Right Click", "Double Click"])
        # Set current click type based on automation settings
        click_index = {
            "none": 0,
            "left": 1,
            "right": 2,
            "double": 3
        }.get(self.automation.click_type, 0)
        self.click_combo.setCurrentIndex(click_index)
        
        click_layout.addWidget(self.click_combo)
        click_group.setLayout(click_layout)
        main_layout.addWidget(click_group)
        
        # Add stretch to push all controls to the top
        main_layout.addStretch(1)
        
        # Connect signals
        self.min_interval_spin.valueChanged.connect(self._update_settings)
        self.max_interval_spin.valueChanged.connect(self._update_settings)
        self.path_combo.currentIndexChanged.connect(self._update_settings)
        self.click_combo.currentIndexChanged.connect(self._update_settings)
    
    def _update_settings(self):
        """Update automation settings based on UI inputs."""
        # Update min interval
        self.automation.min_interval = self.min_interval_spin.value()
        
        # Update max interval (ensure it's >= min interval)
        if self.max_interval_spin.value() < self.automation.min_interval:
            self.max_interval_spin.setValue(self.automation.min_interval)
        self.automation.max_interval = self.max_interval_spin.value()
        
        # Update movement path
        path_mapping = {
            0: "straight",
            1: "zigzag",
            2: "random"
        }
        self.automation.movement_path = path_mapping.get(self.path_combo.currentIndex(), "random")
        
        # Update click type
        click_mapping = {
            0: "none",
            1: "left",
            2: "right",
            3: "double"
        }
        self.automation.click_type = click_mapping.get(self.click_combo.currentIndex(), "none")
        
        # Emit status update
        self.status_update.emit("Mouse settings updated")
    
    def start_automation(self):
        """Start the mouse automation."""
        self._update_settings()
        self.automation.start()
        return True
    
    def stop_automation(self):
        """Stop the mouse automation."""
        self.automation.stop()
    
    def pause_automation(self):
        """Pause the mouse automation."""
        self.automation.pause()
    
    def resume_automation(self):
        """Resume the mouse automation."""
        self.automation.resume()
    
    def reset_settings(self):
        """Reset settings to default values."""
        # Reset to default values
        self.min_interval_spin.setValue(1.0)
        self.max_interval_spin.setValue(3.0)
        self.path_combo.setCurrentIndex(2)  # Random
        self.click_combo.setCurrentIndex(0)  # None
        
        # Update settings
        self._update_settings() 