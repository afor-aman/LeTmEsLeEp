#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QWidget,
    QTextBrowser, QPushButton, QDialogButtonBox
)
from PyQt5.QtCore import Qt


class HelpDialog(QDialog):
    """Dialog providing help and instructions for the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup dialog properties
        self.setWindowTitle("Help")
        self.setMinimumSize(500, 400)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create tabs
        general_tab = self._create_general_tab()
        mouse_tab = self._create_mouse_tab()
        keyboard_tab = self._create_keyboard_tab()
        faq_tab = self._create_faq_tab()
        
        # Add tabs to widget
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(mouse_tab, "Mouse Automation")
        tab_widget.addTab(keyboard_tab, "Keyboard Automation")
        tab_widget.addTab(faq_tab, "FAQ")
        
        # Add tab widget to layout
        main_layout.addWidget(tab_widget)
        
        # Add button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        
        main_layout.addWidget(button_box)
    
    def _create_general_tab(self):
        """Create the general help tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml("""
        <h2>LetMeSleep - Automation Tool</h2>
        <p>This application allows you to simulate human-like interactions with your computer, 
        letting you take a break while maintaining an active presence.</p>
        
        <h3>Main Features</h3>
        <ul>
            <li>Mouse automation with customizable movement patterns</li>
            <li>Keyboard typing simulation with human-like timing</li>
            <li>Easy-to-use interface with pause/resume functionality</li>
            <li>Customizable settings for different scenarios</li>
            <li>Both automations run simultaneously in separate threads</li>
        </ul>
        
        <h3>Getting Started</h3>
        <p>Configure both mouse and keyboard settings, then click "Start Both" to begin automation.</p>
        
        <h3>Failsafe Feature</h3>
        <p><strong>IMPORTANT:</strong> The application includes a critical failsafe mechanism:</p>
        <ul>
            <li><strong>Mouse to Corner:</strong> Move your mouse cursor to the top-left corner (0,0) of your screen to immediately stop all automations</li>
            <li>This failsafe is enabled by default and is highly recommended to keep enabled</li>
            <li>The failsafe provides a quick way to regain control if needed</li>
        </ul>
        
        <h3>Other Safety Features</h3>
        <p>The application includes several additional safety features:</p>
        <ul>
            <li>Timeout option to automatically stop after 30 minutes</li>
            <li>Cursor avoids screen edges to prevent getting stuck</li>
            <li>Easy-to-access stop button to halt automation immediately</li>
            <li>Pause/resume functionality to temporarily stop automation</li>
        </ul>
        """)
        
        layout.addWidget(text_browser)
        return tab
    
    def _create_mouse_tab(self):
        """Create the mouse automation help tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml("""
        <h2>Mouse Automation Help</h2>
        
        <h3>Movement Duration</h3>
        <p>Set the minimum and maximum time (in seconds) for mouse movements:</p>
        <ul>
            <li><strong>Minimum Duration:</strong> Shortest time the mouse takes to move from one point to another</li>
            <li><strong>Maximum Duration:</strong> Longest time the mouse takes to move from one point to another</li>
        </ul>
        <p>The actual movement duration will be randomly selected between these values each time.</p>
        
        <h3>Pause Between Movements</h3>
        <p>Set how long to wait between mouse movements:</p>
        <ul>
            <li><strong>Minimum Pause:</strong> Shortest time to wait after a movement completes before starting the next one</li>
            <li><strong>Maximum Pause:</strong> Longest time to wait after a movement completes before starting the next one</li>
        </ul>
        <p>These settings help create more natural, human-like behavior patterns by adding variability to wait times.</p>
        
        <h3>Movement Path</h3>
        <p>Choose how the mouse cursor will move:</p>
        <ul>
            <li><strong>Straight:</strong> Direct line from one point to another</li>
            <li><strong>ZigZag:</strong> Path with angles that mimic more natural movement</li>
            <li><strong>Random:</strong> Path with random intermediate points (most human-like)</li>
        </ul>
        
        <h3>Click Type</h3>
        <p>Select what kind of mouse click (if any) will occur at destination points:</p>
        <ul>
            <li><strong>None:</strong> Just move the cursor, no clicks</li>
            <li><strong>Left Click:</strong> Perform a left mouse button click</li>
            <li><strong>Right Click:</strong> Perform a right mouse button click</li>
            <li><strong>Double Click:</strong> Perform a double-click with left mouse button</li>
        </ul>
        
        <p><strong>Note:</strong> Be careful when enabling mouse clicks, as they could 
        interact with elements on your screen.</p>
        """)
        
        layout.addWidget(text_browser)
        return tab
    
    def _create_keyboard_tab(self):
        """Create the keyboard automation help tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml("""
        <h2>Keyboard Automation Help</h2>
        
        <h3>Typing Interval</h3>
        <p>Set the minimum and maximum time (in seconds) between keystrokes:</p>
        <ul>
            <li><strong>Minimum Interval:</strong> Fastest typing speed</li>
            <li><strong>Maximum Interval:</strong> Slowest typing speed</li>
        </ul>
        <p>When randomization is enabled, the actual interval will vary between these values.</p>
        
        <h3>Randomize Typing Speed</h3>
        <p>Enable this option to make typing appear more natural:</p>
        <ul>
            <li>When enabled, the delay between keystrokes will vary randomly</li>
            <li>When disabled, keystrokes will occur at a fixed interval (the minimum interval)</li>
        </ul>
        
        <h3>Text to Type</h3>
        <p>Enter the text that will be typed repeatedly:</p>
        <ul>
            <li>The text will be typed character by character</li>
            <li>After typing the entire text, there will be a short pause before repeating</li>
            <li>Choose text appropriate for your application to avoid unwanted effects</li>
        </ul>
        
        <p><strong>Warning:</strong> Be careful when using keyboard automation in text editors or 
        any application that accepts text input, as it could overwrite existing content.</p>
        """)
        
        layout.addWidget(text_browser)
        return tab
    
    def _create_faq_tab(self):
        """Create the FAQ tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml("""
        <h2>Frequently Asked Questions</h2>
        
        <h3>What is the failsafe feature and how does it work?</h3>
        <p>The failsafe is a crucial safety mechanism that allows you to quickly stop all automation 
        by simply moving your mouse cursor to the top-left corner (0,0) of your screen. This provides 
        an emergency stop if the automation is causing problems or if you need to regain control 
        immediately. The failsafe is enabled by default, and we strongly recommend keeping it enabled
        for safety reasons.</p>
        
        <h3>Why are there two different interval settings for mouse movement?</h3>
        <p>The "Movement Duration" controls how long the mouse takes to travel from one point to another,
        while the "Pause Between Movements" controls how long the program waits after completing one movement
        before starting the next one. These separate controls provide more realistic human-like behavior
        and give you fine-tuned control over the simulation pattern.</p>
        
        <h3>Is this software safe to use?</h3>
        <p>Yes, the application is designed to be safe and non-invasive. However, you should be careful 
        when enabling mouse clicks or keyboard typing in applications where unintended interaction could
        cause problems. Always use the failsafe feature and timeout option to ensure the automation stops
        if you need to regain control.</p>
        
        <h3>Why does my screen need to be active for this to work?</h3>
        <p>LetMeSleep simulates user interaction at the system level, which requires an active, 
        unlocked screen to function properly. This is intentional, as it's meant to maintain the 
        appearance of activity.</p>
        
        <h3>Can I customize movement patterns further?</h3>
        <p>The current version offers three movement patterns (straight, zigzag, random) plus customizable
        timing settings. This provides a good balance of flexibility and ease of use. More 
        customization options may be available in future updates.</p>
        
        <h3>Will this prevent my computer from sleeping?</h3>
        <p>The movement and typing should keep your computer awake, but for guaranteed prevention 
        of sleep/screensaver, we recommend also adjusting your system's power settings.</p>
        
        <h3>What happens if both keyboard and mouse automations run at the same time?</h3>
        <p>Both automations run in separate threads, allowing them to operate independently and simultaneously.
        The keyboard automation types text while the mouse moves around your screen. This creates a more
        realistic simulation of human activity than using either automation alone.</p>
        
        <h3>Is there a way to schedule automation?</h3>
        <p>The current version doesn't include scheduling. You need to manually start and stop 
        the automation. This feature may be considered for future updates.</p>
        """)
        
        layout.addWidget(text_browser)
        return tab 