# LetMeSleep

A desktop automation tool that simulates mouse movements and keyboard typing to keep your computer active. Perfect for preventing sleep mode or status changes in applications that track your activity.

## Features

- **Mouse Automation**: Move the mouse in various patterns (straight, zigzag, random) with customizable timing
- **Keyboard Automation**: Type text with customizable timing and randomization
- **Scroll Automation**: Perform random scrolling operations
- **Failsafe**: Move your mouse to the top-left corner (0,0) to immediately stop all automation
- **Combined Control**: Start, stop, and pause both mouse and keyboard automation simultaneously

## Requirements

- Python 3.6 or higher
- PyQt5
- PyAutoGUI
- QDarkTheme

## Installation

### Option 1: Run from Source

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install pyqt5 pyautogui qdarktheme
   ```
3. Run the application:
   ```
   python main.py
   ```

### Option 2: Build a Standalone Application (macOS)

1. Ensure PyInstaller is installed:
   ```
   pip install pyinstaller
   ```
2. Run the build script:
   ```
   ./build_macos.py
   ```
3. The application will be created in the `dist` folder as `LetMeSleep.app`

## Sharing the Application

To share the built application with others:

1. Create a ZIP file of the `dist/LetMeSleep.app` folder
2. Share the ZIP file
3. Recipients will need to:
   - Extract the ZIP file
   - Right-click on the app and select "Open" the first time
   - Possibly approve the app in System Preferences > Security & Privacy

## Usage

1. Configure mouse movement settings:
   - Set movement duration range
   - Set pause times between movements
   - Choose movement pattern (straight, zigzag, random)
   - Enable/disable and configure clicking behavior

2. Configure keyboard typing settings:
   - Set typing interval range
   - Enable/disable randomized typing speed
   - Enter text to be typed (or leave empty for random text)

3. Configure scroll settings:
   - Enable/disable random scrolling
   - Set minimum and maximum scroll amounts

4. Use the controls at the bottom of the window to:
   - Start both automations
   - Pause/resume both automations
   - Reset all settings to defaults
   - Exit the application

5. The status bar at the bottom shows the current state and any error messages.

## Safety Features

- Move your mouse to the top-left corner (0,0) to stop all automation immediately
- Use the "Enable failsafe" checkbox to toggle this safety feature

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is intended for legitimate use cases like preventing system sleep or maintaining active status. Use responsibly and in accordance with applicable policies and regulations. 