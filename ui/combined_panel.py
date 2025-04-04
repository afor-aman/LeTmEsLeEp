#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QFormLayout, QGridLayout,
    QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal

from automation import MouseAutomation, KeyboardAutomation


class CombinedPanel(QWidget):
    """Panel that combines mouse and keyboard automation settings."""
    
    # Signal for status updates
    status_update = pyqtSignal(str)
    failsafe_triggered = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize automation
        self.mouse_automation = MouseAutomation()
        self.keyboard_automation = KeyboardAutomation()
        
        # Connect status signals
        self.mouse_automation.status_update.connect(self._forward_status)
        self.keyboard_automation.status_update.connect(self._forward_status)
        
        # Connect failsafe signals
        self.mouse_automation.failsafe_triggered.connect(self._handle_failsafe)
        self.keyboard_automation.failsafe_triggered.connect(self._handle_failsafe)
        
        # Connect error signals
        self.mouse_automation.error_occurred.connect(self._forward_error)
        self.keyboard_automation.error_occurred.connect(self._forward_error)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Failsafe info at the top
        failsafe_frame = QFrame()
        failsafe_frame.setFrameShape(QFrame.StyledPanel)
        failsafe_frame.setFrameShadow(QFrame.Raised)
        failsafe_layout = QVBoxLayout(failsafe_frame)
        
        failsafe_label = QLabel("FAILSAFE: Move mouse to top-left corner (0,0) to immediately stop all automation")
        failsafe_label.setStyleSheet("color: red; font-weight: bold;")
        failsafe_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        failsafe_layout.addWidget(failsafe_label)
        
        self.failsafe_check = QCheckBox("Enable failsafe (recommended)")
        self.failsafe_check.setChecked(True)
        self.failsafe_check.stateChanged.connect(self._update_failsafe)
        failsafe_layout.addWidget(self.failsafe_check)
        
        main_layout.addWidget(failsafe_frame)
        
        # Mouse and keyboard settings side by side
        settings_layout = QHBoxLayout()
        
        # Mouse settings
        mouse_layout = QVBoxLayout()
        
        # Mouse title
        mouse_title = QLabel("Mouse Automation")
        mouse_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mouse_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        mouse_layout.addWidget(mouse_title)
        
        # Mouse movement interval settings group
        mouse_interval_group = QGroupBox("Movement Duration (seconds)")
        mouse_interval_layout = QFormLayout()
        
        # Min interval input
        self.mouse_min_interval_spin = QDoubleSpinBox()
        self.mouse_min_interval_spin.setRange(0.1, 10.0)
        self.mouse_min_interval_spin.setSingleStep(0.1)
        self.mouse_min_interval_spin.setValue(self.mouse_automation.min_interval)
        mouse_interval_layout.addRow("Minimum Duration:", self.mouse_min_interval_spin)
        
        # Max interval input
        self.mouse_max_interval_spin = QDoubleSpinBox()
        self.mouse_max_interval_spin.setRange(0.1, 10.0)
        self.mouse_max_interval_spin.setSingleStep(0.1)
        self.mouse_max_interval_spin.setValue(self.mouse_automation.max_interval)
        mouse_interval_layout.addRow("Maximum Duration:", self.mouse_max_interval_spin)
        
        mouse_interval_group.setLayout(mouse_interval_layout)
        mouse_layout.addWidget(mouse_interval_group)
        
        # Between mouse movements interval settings group
        between_interval_group = QGroupBox("Pause Between Movements (seconds)")
        between_interval_layout = QFormLayout()
        
        # Between min interval input
        self.between_min_interval_spin = QDoubleSpinBox()
        self.between_min_interval_spin.setRange(0.1, 30.0)
        self.between_min_interval_spin.setSingleStep(0.5)
        self.between_min_interval_spin.setValue(self.mouse_automation.between_min_interval)
        between_interval_layout.addRow("Minimum Pause:", self.between_min_interval_spin)
        
        # Between max interval input
        self.between_max_interval_spin = QDoubleSpinBox()
        self.between_max_interval_spin.setRange(0.1, 60.0)
        self.between_max_interval_spin.setSingleStep(0.5)
        self.between_max_interval_spin.setValue(self.mouse_automation.between_max_interval)
        between_interval_layout.addRow("Maximum Pause:", self.between_max_interval_spin)
        
        between_interval_group.setLayout(between_interval_layout)
        mouse_layout.addWidget(between_interval_group)
        
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
        }.get(self.mouse_automation.movement_path, 2)
        self.path_combo.setCurrentIndex(path_index)
        
        path_layout.addWidget(self.path_combo)
        path_group.setLayout(path_layout)
        mouse_layout.addWidget(path_group)
        
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
        }.get(self.mouse_automation.click_type, 0)
        self.click_combo.setCurrentIndex(click_index)
        
        click_layout.addWidget(self.click_combo)
        click_group.setLayout(click_layout)
        mouse_layout.addWidget(click_group)
        
        # Scroll settings group
        scroll_group = QGroupBox("Scroll Settings")
        scroll_layout = QVBoxLayout()
        
        # Enable scrolling checkbox
        self.enable_scroll_check = QCheckBox("Enable Random Scrolling")
        self.enable_scroll_check.setChecked(self.mouse_automation.enable_scrolling)
        scroll_layout.addWidget(self.enable_scroll_check)
        
        # Scroll amount range
        scroll_amount_layout = QFormLayout()
        
        self.scroll_min_amount_spin = QSpinBox()
        self.scroll_min_amount_spin.setRange(-20, 0)  # Negative values for scrolling down
        self.scroll_min_amount_spin.setValue(self.mouse_automation.scroll_min_amount)
        self.scroll_min_amount_spin.setToolTip("Minimum scroll amount (negative values scroll down)")
        scroll_amount_layout.addRow("Min Scroll Amount:", self.scroll_min_amount_spin)
        
        self.scroll_max_amount_spin = QSpinBox()
        self.scroll_max_amount_spin.setRange(0, 20)  # Positive values for scrolling up
        self.scroll_max_amount_spin.setValue(self.mouse_automation.scroll_max_amount)
        self.scroll_max_amount_spin.setToolTip("Maximum scroll amount (positive values scroll up)")
        scroll_amount_layout.addRow("Max Scroll Amount:", self.scroll_max_amount_spin)
        
        scroll_layout.addLayout(scroll_amount_layout)
        
        scroll_group.setLayout(scroll_layout)
        mouse_layout.addWidget(scroll_group)
        
        # Add stretch to push all controls to the top
        mouse_layout.addStretch(1)
        
        # Keyboard settings
        keyboard_layout = QVBoxLayout()
        
        # Keyboard title
        keyboard_title = QLabel("Keyboard Automation")
        keyboard_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        keyboard_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        keyboard_layout.addWidget(keyboard_title)
        
        # Keyboard interval settings group
        keyboard_interval_group = QGroupBox("Typing Interval (seconds)")
        keyboard_interval_layout = QFormLayout()
        
        # Min interval input
        self.keyboard_min_interval_spin = QDoubleSpinBox()
        self.keyboard_min_interval_spin.setRange(0.01, 1.0)
        self.keyboard_min_interval_spin.setSingleStep(0.01)
        self.keyboard_min_interval_spin.setValue(self.keyboard_automation.min_interval)
        keyboard_interval_layout.addRow("Minimum Interval:", self.keyboard_min_interval_spin)
        
        # Max interval input
        self.keyboard_max_interval_spin = QDoubleSpinBox()
        self.keyboard_max_interval_spin.setRange(0.01, 1.0)
        self.keyboard_max_interval_spin.setSingleStep(0.01)
        self.keyboard_max_interval_spin.setValue(self.keyboard_automation.max_interval)
        keyboard_interval_layout.addRow("Maximum Interval:", self.keyboard_max_interval_spin)
        
        # Randomize checkbox
        self.randomize_check = QCheckBox("Randomize Typing Speed")
        self.randomize_check.setChecked(self.keyboard_automation.randomize_typing)
        keyboard_interval_layout.addRow("", self.randomize_check)
        
        keyboard_interval_group.setLayout(keyboard_interval_layout)
        keyboard_layout.addWidget(keyboard_interval_group)
        
        # Text input group
        text_group = QGroupBox("Text to Type")
        text_layout = QVBoxLayout()
        
        # Text input
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter text to type...")
        self.text_edit.setText(self.keyboard_automation.text_to_type)
        
        text_layout.addWidget(self.text_edit)
        text_group.setLayout(text_layout)
        keyboard_layout.addWidget(text_group)
        
        # Add stretch to push all controls to the top
        keyboard_layout.addStretch(1)
        
        # Add mouse and keyboard layouts to settings layout
        settings_layout.addLayout(mouse_layout)
        settings_layout.addLayout(keyboard_layout)
        
        # Add settings layout to main layout
        main_layout.addLayout(settings_layout)
        
        # Connect signals
        self.mouse_min_interval_spin.valueChanged.connect(self._update_mouse_settings)
        self.mouse_max_interval_spin.valueChanged.connect(self._update_mouse_settings)
        self.between_min_interval_spin.valueChanged.connect(self._update_mouse_settings)
        self.between_max_interval_spin.valueChanged.connect(self._update_mouse_settings)
        self.path_combo.currentIndexChanged.connect(self._update_mouse_settings)
        self.click_combo.currentIndexChanged.connect(self._update_mouse_settings)
        self.enable_scroll_check.stateChanged.connect(self._update_mouse_settings)
        self.scroll_min_amount_spin.valueChanged.connect(self._update_mouse_settings)
        self.scroll_max_amount_spin.valueChanged.connect(self._update_mouse_settings)
        
        self.keyboard_min_interval_spin.valueChanged.connect(self._update_keyboard_settings)
        self.keyboard_max_interval_spin.valueChanged.connect(self._update_keyboard_settings)
        self.randomize_check.stateChanged.connect(self._update_keyboard_settings)
        self.text_edit.textChanged.connect(self._update_keyboard_text)
    
    def _handle_failsafe(self):
        """Handle failsafe triggered event."""
        self.stop_automation()
        self.failsafe_triggered.emit()
    
    def _update_failsafe(self):
        """Update failsafe settings based on UI input."""
        is_active = self.failsafe_check.isChecked()
        self.mouse_automation.set_failsafe_active(is_active)
        self.keyboard_automation.set_failsafe_active(is_active)
        
        status = "enabled" if is_active else "disabled"
        self.status_update.emit(f"Failsafe {status}")
    
    def _forward_status(self, message):
        """Forward status updates from automations."""
        self.status_update.emit(message)
    
    def _forward_error(self, message):
        """Forward error messages from automations."""
        self.error_occurred.emit(message)
    
    def _update_mouse_settings(self):
        """Update mouse automation settings based on UI inputs."""
        # Update min interval
        self.mouse_automation.min_interval = self.mouse_min_interval_spin.value()
        
        # Update max interval (ensure it's >= min interval)
        if self.mouse_max_interval_spin.value() < self.mouse_automation.min_interval:
            self.mouse_max_interval_spin.setValue(self.mouse_automation.min_interval)
        self.mouse_automation.max_interval = self.mouse_max_interval_spin.value()
        
        # Update between movement intervals
        self.mouse_automation.between_min_interval = self.between_min_interval_spin.value()
        
        # Update between max interval (ensure it's >= between min interval)
        if self.between_max_interval_spin.value() < self.mouse_automation.between_min_interval:
            self.between_max_interval_spin.setValue(self.mouse_automation.between_min_interval)
        self.mouse_automation.between_max_interval = self.between_max_interval_spin.value()
        
        # Update movement path
        path_mapping = {
            0: "straight",
            1: "zigzag",
            2: "random"
        }
        self.mouse_automation.movement_path = path_mapping.get(self.path_combo.currentIndex(), "random")
        
        # Update click type
        click_mapping = {
            0: "none",
            1: "left",
            2: "right",
            3: "double"
        }
        self.mouse_automation.click_type = click_mapping.get(self.click_combo.currentIndex(), "none")
        
        # Update scroll settings
        self.mouse_automation.enable_scrolling = self.enable_scroll_check.isChecked()
        self.mouse_automation.scroll_min_amount = self.scroll_min_amount_spin.value()
        self.mouse_automation.scroll_max_amount = self.scroll_max_amount_spin.value()
        
        # Emit status update
        self.status_update.emit("Mouse settings updated")
    
    def _update_keyboard_settings(self):
        """Update keyboard automation settings based on UI inputs."""
        # Update min interval
        self.keyboard_automation.min_interval = self.keyboard_min_interval_spin.value()
        
        # Update max interval (ensure it's >= min interval)
        if self.keyboard_max_interval_spin.value() < self.keyboard_automation.min_interval:
            self.keyboard_max_interval_spin.setValue(self.keyboard_automation.min_interval)
        self.keyboard_automation.max_interval = self.keyboard_max_interval_spin.value()
        
        # Update randomize setting
        self.keyboard_automation.randomize_typing = self.randomize_check.isChecked()
        
        # Emit status update
        self.status_update.emit("Keyboard settings updated")
    
    def _validate_settings(self):
        """Validate all settings before starting automation."""
        # Validate mouse settings
        if self.mouse_min_interval_spin.value() > self.mouse_max_interval_spin.value():
            self.error_occurred.emit("Mouse minimum interval cannot be greater than maximum interval")
            return False
            
        if self.between_min_interval_spin.value() > self.between_max_interval_spin.value():
            self.error_occurred.emit("Between movement minimum interval cannot be greater than maximum interval")
            return False
            
        # Validate scroll settings
        if self.enable_scroll_check.isChecked():
            if self.scroll_min_amount_spin.value() > self.scroll_max_amount_spin.value():
                self.error_occurred.emit("Scroll minimum amount cannot be greater than maximum amount")
                return False
        
        # Validate keyboard settings
        if self.keyboard_min_interval_spin.value() > self.keyboard_max_interval_spin.value():
            self.error_occurred.emit("Keyboard minimum interval cannot be greater than maximum interval")
            return False
            
        # No longer validate for empty text - we'll generate random text if empty
        
        return True
    
    def _generate_random_text(self):
        """Generate random text for typing when none is provided."""
        random_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "All that glitters is not gold.",
            "The early bird catches the worm.",
            "A penny saved is a penny earned.",
            "Actions speak louder than words.",
            "Don't count your chickens before they hatch.",
            "Every cloud has a silver lining.",
            "It's raining cats and dogs.",
            "You can't judge a book by its cover."
        ]
        import random
        return random.choice(random_texts)

    def _update_keyboard_text(self):
        """Update text to type."""
        text = self.text_edit.toPlainText().strip()
        if not text:
            # If no text is provided, use random text
            text = self._generate_random_text()
            self.status_update.emit(f"No text provided. Using random text: '{text}'")
            # Update the text field with the random text
            self.text_edit.setText(text)
        
        self.keyboard_automation.text_to_type = text
    
    def start_automation(self):
        """Start both automations."""
        self._update_mouse_settings()
        self._update_keyboard_settings()
        self._update_keyboard_text()
        self._update_failsafe()
        
        # Validate settings before starting
        if not self._validate_settings():
            return False
        
        # Start both automations
        mouse_success = self.mouse_automation.start()
        keyboard_success = self.keyboard_automation.start()
        
        if not mouse_success or not keyboard_success:
            # If either start failed, stop both
            self.stop_automation()
            self.error_occurred.emit("Failed to start one or more automations")
            return False
        
        self.status_update.emit("Both automations started")
        return True
    
    def stop_automation(self):
        """Stop both automations."""
        self.mouse_automation.stop()
        self.keyboard_automation.stop()
        self.status_update.emit("Both automations stopped")
    
    def pause_automation(self):
        """Pause both automations."""
        self.mouse_automation.pause()
        self.keyboard_automation.pause()
        self.status_update.emit("Both automations paused")
    
    def resume_automation(self):
        """Resume both automations."""
        self.mouse_automation.resume()
        self.keyboard_automation.resume()
        self.status_update.emit("Both automations resumed")
    
    def reset_settings(self):
        """Reset all settings to default values."""
        # Reset mouse settings
        self.mouse_min_interval_spin.setValue(1.0)
        self.mouse_max_interval_spin.setValue(3.0)
        self.between_min_interval_spin.setValue(2.0)
        self.between_max_interval_spin.setValue(5.0)
        self.path_combo.setCurrentIndex(2)  # Random
        self.click_combo.setCurrentIndex(0)  # None
        self.enable_scroll_check.setChecked(False)
        self.scroll_min_amount_spin.setValue(-5)
        self.scroll_max_amount_spin.setValue(5)
        
        # Reset keyboard settings
        self.keyboard_min_interval_spin.setValue(0.1)
        self.keyboard_max_interval_spin.setValue(0.3)
        self.randomize_check.setChecked(True)
        self.text_edit.setText("The quick brown fox jumps over the lazy dog.")
        
        # Reset failsafe
        self.failsafe_check.setChecked(True)
        
        # Update settings
        self._update_mouse_settings()
        self._update_keyboard_settings()
        self._update_keyboard_text()
        self._update_failsafe()
        
        self.status_update.emit("All settings reset to default") 