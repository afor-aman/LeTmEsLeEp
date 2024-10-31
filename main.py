from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QLineEdit,
    QCheckBox,
    QSizePolicy,
    QSpacerItem,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QDialog,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
import sys
from utils.printer_thread import PrinterThread


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Help")
        self.setGeometry(200, 200, 550, 500)
        self.setFixedSize(550, 500)

        # Set the dialog style to match the main window
        self.setStyleSheet(
            """
            QDialog {
                background-color: #2c2c2c;
            }
            QTextEdit {
                background-color: rgba(60, 60, 60, 200);
                color: #ffffff;
                border: none;
            }
            QPushButton {
                background-color: rgba(70, 130, 180, 200);
                color: #ffffff;
                padding: 8px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:disabled {
                background-color: rgba(120, 120, 120, 200);
                color: #888888;
            }
        """
        )

        # Create a layout for the dialog
        layout = QVBoxLayout()

        # Create a text edit to display help information
        help_text = """
        Help Information:

        - Minimum and Maximum Mouse Movement Delay: 
          Set the delays for mouse movements in milliseconds.

        - Randomize Scroll: 
          Check this box to randomize mouse scroll behavior.

        - Words Per Minute (WPM): 
          Enter the desired typing speed.

        - Minimum and Maximum Typing Delay: 
          Set the delays for typing in milliseconds.

        - Tab Change Delay: 
          Set the delays for changing tabs.

        NOTE: All Delays are in ms(micro-second) and decimal values are accepted\n
        Use the Start button to begin and Stop to end the process.
        """

        text_edit = QTextEdit()
        text_edit.setPlainText(help_text)
        text_edit.setReadOnly(True)  # Make it read-only
        layout.addWidget(text_edit)

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)  # Close the dialog when clicked
        layout.addWidget(close_button)

        self.setLayout(layout)

class SettingsUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 500, 750)
        self.setFixedSize(510, 750)

        # Apply a dark and glassy style
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2c2c2c;
            }
            QWidget {
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
            QGroupBox {
                background-color: rgba(50, 50, 50, 200);
                border: 1px solid rgba(200, 200, 200, 100);
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit {
                background-color: rgba(60, 60, 60, 200);
                color: #ffffff;
                padding: 5px;
                border: 1px solid rgba(200, 200, 200, 150);
                border-radius: 4px;
            }
            QCheckBox {
                color: #ffffff;
            }
            QPushButton {
                background-color: rgba(70, 130, 180, 200);
                color: #ffffff;
                padding: 8px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:disabled {
                background-color: rgba(120, 120, 120, 200);
                color: #888888;
            }
            QLabel {
                margin-right: 10px;
            }
        """
        )

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(main_layout)

        # Help Button
        self.help_icon_label = QLabel()
        self.load_svg_icon_help(
            "./icons/help.svg", self.help_icon_label
        )  # Load the help SVG icon
        self.help_icon_label.mousePressEvent = (
            self.show_help
        )  # Connect mouse press to show help
        main_layout.addWidget(
            self.help_icon_label, alignment=Qt.AlignmentFlag.AlignRight
        )

        # Mouse Settings Section
        mouse_settings_group = QGroupBox()
        mouse_layout = QGridLayout()
        mouse_settings_group.setLayout(mouse_layout)

        # Load SVG icon for Mouse Settings
        self.mouse_icon_label = QLabel()
        self.load_svg_icon("./icons/mouse.svg", self.mouse_icon_label)
        mouse_layout.addWidget(self.mouse_icon_label, 0, 0, 1, 1)

        # Mouse Settings Label
        mouse_settings_label = QLabel("Mouse Settings")
        mouse_settings_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mouse_layout.addWidget(mouse_settings_label, 0, 1)

        # Minimum delay for mouse movement
        self.min_mouse_delay_label = QLabel("Minimum Mouse Movement Delay (ms):")
        self.min_mouse_delay_input = QLineEdit("10")  # Initial value
        self.min_mouse_delay_input.setPlaceholderText("Enter min delay")
        self.min_mouse_delay_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        mouse_layout.addWidget(self.min_mouse_delay_label, 1, 0)
        mouse_layout.addWidget(self.min_mouse_delay_input, 1, 1)

        # Maximum delay for mouse movement
        self.max_mouse_delay_label = QLabel("Maximum Mouse Movement Delay (ms):")
        self.max_mouse_delay_input = QLineEdit("10")  # Initial value
        self.max_mouse_delay_input.setPlaceholderText("Enter max delay")
        self.max_mouse_delay_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        mouse_layout.addWidget(self.max_mouse_delay_label, 2, 0)
        mouse_layout.addWidget(self.max_mouse_delay_input, 2, 1)

        # Randomize scroll checkbox
        self.randomize_scroll_checkbox = QCheckBox("Randomize Scroll")
        mouse_layout.addWidget(self.randomize_scroll_checkbox, 3, 0, 1, 2)

        # Add mouse settings to the main layout
        main_layout.addWidget(mouse_settings_group)

        # Spacer between sections
        main_layout.addSpacerItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Keyboard Settings Section
        keyboard_settings_group = QGroupBox()
        keyboard_layout = QGridLayout()
        keyboard_settings_group.setLayout(keyboard_layout)

        # Load SVG icon for Keyboard Settings
        self.keyboard_icon_label = QLabel()
        self.load_svg_icon("./icons/keyboard.svg", self.keyboard_icon_label)
        keyboard_layout.addWidget(self.keyboard_icon_label, 0, 0, 1, 1)

        # Keyboard Settings Label
        keyboard_settings_label = QLabel("Keyboard Settings")
        keyboard_settings_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        keyboard_layout.addWidget(keyboard_settings_label, 0, 1)

        # WPM input field
        self.wpm_input = QLineEdit()
        self.wpm_input.setPlaceholderText("Enter WPM")
        self.wpm_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change
        keyboard_layout.addWidget(QLabel("Words Per Minute (WPM):"), 1, 0)
        keyboard_layout.addWidget(self.wpm_input, 1, 1)

        # Minimum delay for active typing
        self.min_delay_label = QLabel("Minimum Typing Delay (ms):")
        self.min_delay_input = QLineEdit("10")  # Initial value
        self.min_delay_input.setPlaceholderText("Enter min delay")
        self.min_delay_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        keyboard_layout.addWidget(self.min_delay_label, 2, 0)
        keyboard_layout.addWidget(self.min_delay_input, 2, 1)

        # Maximum delay for active typing
        self.max_delay_label = QLabel("Maximum Typing Delay (ms):")
        self.max_delay_input = QLineEdit("10")  # Initial value
        self.max_delay_input.setPlaceholderText("Enter max delay")
        self.max_delay_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        keyboard_layout.addWidget(self.max_delay_label, 3, 0)
        keyboard_layout.addWidget(self.max_delay_input, 3, 1)

        # Add keyboard settings to the main layout
        main_layout.addWidget(keyboard_settings_group)

        # Spacer between sections
        main_layout.addSpacerItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Tab Change Settings Section
        tab_change_settings_group = QGroupBox()
        tab_change_layout = QGridLayout()
        tab_change_settings_group.setLayout(tab_change_layout)

        # Load SVG icon for Tab Change Settings
        self.tab_change_icon_label = QLabel()
        self.load_svg_icon("./icons/tabs.svg", self.tab_change_icon_label)
        tab_change_layout.addWidget(self.tab_change_icon_label, 0, 0, 1, 1)

        # Tab Change Settings Label
        tab_change_settings_label = QLabel("Tab Change Settings")
        tab_change_settings_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_change_layout.addWidget(tab_change_settings_label, 0, 1)

        # Minimum delay for tab change
        self.min_tab_change_label = QLabel("Minimum Tab Change Delay (ms):")
        self.min_tab_change_input = QLineEdit("10")  # Initial value
        self.min_tab_change_input.setPlaceholderText("Enter min delay")
        self.min_tab_change_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        tab_change_layout.addWidget(self.min_tab_change_label, 1, 0)
        tab_change_layout.addWidget(self.min_tab_change_input, 1, 1)

        # Maximum delay for tab change
        self.max_tab_change_label = QLabel("Maximum Tab Change Delay (ms):")
        self.max_tab_change_input = QLineEdit("10")  # Initial value
        self.max_tab_change_input.setPlaceholderText("Enter max delay")
        self.max_tab_change_input.textChanged.connect(
            self.validate_input
        )  # Validate on text change

        tab_change_layout.addWidget(self.max_tab_change_label, 2, 0)
        tab_change_layout.addWidget(self.max_tab_change_input, 2, 1)

        # Add tab change settings to the main layout
        main_layout.addWidget(tab_change_settings_group)

        # Spacer between sections
        main_layout.addSpacerItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Control Buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setDisabled(True)  # Disable the Stop button initially

        # Connect buttons to their actions
        self.start_button.clicked.connect(self.start_action)
        self.stop_button.clicked.connect(self.stop_action)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Initialize the printer thread
        self.printer_thread = None
        
        self.key_sequence = []
        self.sequence_timer = QTimer(self)
        self.sequence_timer.setInterval(500)  # 500 ms to reset the sequence
        self.sequence_timer.timeout.connect(self.reset_key_sequence)
        
        emergency_note = QLabel("Press Ctrl+K+L for emergency stop.")
        emergency_note.setStyleSheet("color: #AAAAAA; font-size: 12.5pt;")  # Style to match UI
        emergency_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(emergency_note)  # Add the n

    def keyPressEvent(self, event):
        """Override to handle key sequence for emergency stop (Ctrl+K+L)."""
        key = event.key()

        # Track if Ctrl is pressed, followed by K, then L
        if key == Qt.Key.Key_Control and not self.key_sequence:
            self.key_sequence.append("Ctrl")
        elif key == Qt.Key.Key_K and "Ctrl" in self.key_sequence and "K" not in self.key_sequence:
            self.key_sequence.append("K")
        elif key == Qt.Key.Key_L and "K" in self.key_sequence:
            self.key_sequence.append("L")
            # If sequence Ctrl+K+L is complete, stop the app
            if self.key_sequence == ["Ctrl", "K", "L"]:
                self.emergency_stop()
                return

        # Restart the timer to check for sequence timeout
        self.sequence_timer.start()

    def keyReleaseEvent(self, event):
        """Override to handle key release (reset if Ctrl is released)."""
        if event.key() == Qt.Key.Key_Control:
            self.reset_key_sequence()

    def reset_key_sequence(self):
        """Reset the key sequence and stop the timer."""
        self.key_sequence.clear()
        self.sequence_timer.stop()

    def emergency_stop(self):
        """Terminate the application safely on emergency shortcut."""
        self.reset_key_sequence()
        
        # Stop any active threads or resources
        if self.printer_thread and self.printer_thread.isRunning():
            self.printer_thread.stop()  # Safely stop the thread
            self.printer_thread.wait()  # Wait for it to finish

        # Close the application gracefully
        QApplication.quit()

    def show_help(self, event):
        """Show the help dialog when the help icon is clicked."""
        help_dialog = HelpDialog()
        help_dialog.exec()  # Show the dialog modally

    def load_svg_icon(self, file_path, label):
        """Load an SVG icon from the given file path and set it to the label."""
        svg_renderer = QSvgRenderer(file_path)
        pixmap = QPixmap(48, 48)  # Adjust size as necessary
        pixmap.fill(Qt.GlobalColor.transparent)  # Fill with transparent background
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        label.setPixmap(pixmap)

    def load_svg_icon_help(self, file_path, label):
        """Load an SVG icon from the given file path and set it to the label."""
        svg_renderer = QSvgRenderer(file_path)
        pixmap = QPixmap(20, 20)  # Adjust size as necessary
        pixmap.fill(Qt.GlobalColor.transparent)  # Fill with transparent background
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        label.setPixmap(pixmap)

    def start_action(self):
        """Handle the start button click event."""
        self.start_button.setDisabled(True)  # Disable the Start button
        self.stop_button.setEnabled(True)  # Enable the Stop button

        # Create a new instance of the PrinterThread
        self.printer_thread = PrinterThread()
        self.printer_thread.update_signal.connect(
            self.print_number
        )  # Connect the signal to the slot
        self.printer_thread.start()  # Start the printer thread

    def stop_action(self):
        """Handle the stop button click event."""
        self.start_button.setEnabled(True)  # Enable the Start button
        self.stop_button.setDisabled(True)  # Disable the Stop button
        print("Stopped")  # Placeholder for the stop action
        if self.printer_thread:  # Check if the thread is running
            self.printer_thread.stop()  # Stop the thread gracefully
            self.printer_thread.wait()  # Wait for the thread to finish
            self.printer_thread = None  # Clear the reference

    def print_number(self, number):
        """Update the GUI with the current number."""
        print(number)  # Print the number to console or update a label if needed

    def validate_input(self):
        """Validate the input to ensure it's a valid float or int."""
        inputs = [
            self.min_mouse_delay_input,
            self.max_mouse_delay_input,
            self.wpm_input,
            self.min_delay_input,
            self.max_delay_input,
            self.min_tab_change_input,
            self.max_tab_change_input
        ]

        for input_field in inputs:
            value = input_field.text()
            if value:  # Only validate if there's something entered
                try:
                    num_value = float(value)  # Convert to float
                    # Validate min/max delays (1 ms to 10,000 ms)
                    if input_field in [self.min_mouse_delay_input, self.max_mouse_delay_input,
                                       self.min_delay_input, self.max_delay_input,
                                       self.min_tab_change_input, self.max_tab_change_input]:
                        if num_value < 1 or num_value > 10000:  # Validate min/max delay
                            self.show_warning("The delay must be between 1 ms and 10,000 ms.")
                            input_field.clear()  # Clear the invalid input
                    # Validate WPM (max 50)
                    elif input_field == self.wpm_input:
                        if num_value > 50:  # Validate WPM
                            self.show_warning("WPM must not exceed 50.")
                            input_field.clear()  # Clear the invalid input
                except ValueError:
                    # Show a warning message if conversion fails
                    self.show_warning(f"The entered value '{value}' is not a valid number.")
                    input_field.clear()  # Clear the invalid input

    def show_warning(self, message):
        """Display a warning message in a popup with black text."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Input Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Apply stylesheet for black text in the message box
        msg_box.setStyleSheet("""
            QLabel {
                font-size: 12.5pt;
            }
            QPushButton {
                background-color: rgba(70, 130, 180, 200);
                color: #ffffff;
                padding: 8px;
                border-radius: 4px;
            }
        """)

        msg_box.exec()  # Show the message box


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsUI()
    window.show()
    sys.exit(app.exec())
