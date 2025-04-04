#!/usr/bin/env python3
import time
import random
import threading
import logging
import sys
import pyautogui
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

# Set up PyAutoGUI failsafe
pyautogui.FAILSAFE = True  # Moving mouse to corner (0,0) will abort

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LetMeSleep")


class AutomationError(Exception):
    """Base class for automation-related exceptions."""
    pass


class PermissionError(AutomationError):
    """Exception raised when there are permission issues with input control."""
    pass


class AutomationBase(QObject):
    """Base class for automation with threading and signals."""
    status_update = pyqtSignal(str)
    failsafe_triggered = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.paused = False
        self.thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Not paused by default
        self.failsafe_active = True
        self.error_count = 0
        self.max_error_retries = 3
        
    def _handle_error(self, exception, is_fatal=False):
        """Handle errors during automation."""
        error_msg = f"Error: {str(exception)}"
        logger.error(error_msg)
        self.error_occurred.emit(error_msg)
        
        if is_fatal:
            self.running = False
            self._stop_event.set()
            return False
        
        self.error_count += 1
        if self.error_count >= self.max_error_retries:
            error_msg = f"Maximum error retries ({self.max_error_retries}) exceeded. Stopping automation."
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            self.running = False
            self._stop_event.set()
            return False
            
        # Pause briefly after an error
        time.sleep(1.0)
        return True

    def start(self):
        """Start the automation thread."""
        try:
            if self.thread and self.thread.is_alive():
                self.status_update.emit("Automation is already running")
                return False
                
            self.running = True
            self.error_count = 0
            self._stop_event.clear()
            self._pause_event.set()
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()
            return True
        except Exception as e:
            error_msg = f"Failed to start automation: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
    def stop(self):
        """Stop the automation thread."""
        try:
            self.running = False
            self._stop_event.set()
            self._pause_event.set()  # Ensure thread is not paused when stopping
            if self.thread and self.thread.is_alive():
                self.thread.join(2.0)
                if self.thread.is_alive():
                    logger.warning("Thread did not terminate within timeout")
            return True
        except Exception as e:
            error_msg = f"Error stopping automation: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
            
    def pause(self):
        """Pause the automation."""
        try:
            if not self.running:
                self.status_update.emit("Automation is not running")
                return False
                
            self.paused = True
            self._pause_event.clear()
            self.status_update.emit("Automation paused")
            return True
        except Exception as e:
            error_msg = f"Error pausing automation: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
    def resume(self):
        """Resume the automation."""
        try:
            if not self.running:
                self.status_update.emit("Automation is not running")
                return False
                
            if not self.paused:
                self.status_update.emit("Automation is not paused")
                return False
                
            self.paused = False
            self._pause_event.set()
            self.status_update.emit("Automation resumed")
            return True
        except Exception as e:
            error_msg = f"Error resuming automation: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
    def is_running(self):
        """Check if automation is running."""
        return self.running
        
    def is_paused(self):
        """Check if automation is paused."""
        return self.paused
    
    def set_failsafe_active(self, active):
        """Set whether failsafe is active."""
        self.failsafe_active = active
        
    def _check_failsafe(self):
        """Check if failsafe should be triggered."""
        if not self.failsafe_active:
            return False
        
        try:
            # Check current position for failsafe
            x, y = pyautogui.position()
            if x == 0 and y == 0:
                self.status_update.emit("Failsafe triggered! Stopping automation.")
                self.failsafe_triggered.emit()
                return True
        except:
            pass
        return False
        
    def _run(self):
        """Main run method to be implemented by subclasses."""
        pass


class MouseAutomation(AutomationBase):
    """Class to handle mouse movement automation."""
    
    def __init__(self):
        super().__init__()
        # Default settings
        self.min_interval = 1.0
        self.max_interval = 3.0
        self.between_min_interval = 2.0
        self.between_max_interval = 5.0
        self.movement_path = "random"  # Options: "straight", "zigzag", "random"
        self.click_type = "none"  # Options: "none", "left", "right", "double"
        # Scroll settings
        self.enable_scrolling = False
        self.scroll_min_interval = 1.0
        self.scroll_max_interval = 3.0
        self.scroll_min_amount = -5  # Negative values scroll down
        self.scroll_max_amount = 5   # Positive values scroll up
    
    def _check_failsafe(self):
        """Check if mouse is in a failsafe position (top-left corner)."""
        if not self.failsafe_active:
            return False
            
        try:
            x, y = pyautogui.position()
            if x < 5 and y < 5:  # If mouse in top-left corner
                self.status_update.emit("Failsafe triggered: Mouse in corner")
                self.failsafe_triggered.emit()
                return True
        except Exception as e:
            logger.warning(f"Error checking failsafe: {str(e)}")
        
        return False
    
    def _safe_move(self, x, y, duration):
        """Safely move the mouse with error handling."""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except pyautogui.PyAutoGUIException as e:
            return self._handle_error(e)
        except Exception as e:
            return self._handle_error(e)
    
    def _safe_click(self):
        """Safely perform mouse click with error handling."""
        try:
            if self.click_type == "left":
                pyautogui.click()
            elif self.click_type == "right":
                pyautogui.rightClick()
            elif self.click_type == "double":
                pyautogui.doubleClick()
            return True
        except pyautogui.PyAutoGUIException as e:
            return self._handle_error(e)
        except Exception as e:
            return self._handle_error(e)
    
    def _safe_scroll(self, amount):
        """Safely scroll the mouse wheel with error handling."""
        try:
            pyautogui.scroll(amount)
            return True
        except pyautogui.PyAutoGUIException as e:
            return self._handle_error(e)
        except Exception as e:
            return self._handle_error(e)
    
    def _run(self):
        """Main loop for mouse automation."""
        try:
            # Get screen dimensions
            try:
                screen_width, screen_height = pyautogui.size()
            except Exception as e:
                error_msg = f"Failed to get screen size: {str(e)}"
                logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                self.running = False
                return
            
            self.status_update.emit(f"Mouse automation started (Screen size: {screen_width}x{screen_height})")
            
            # Track when to perform the next action
            next_action_time = time.time()
            
            while not self._stop_event.is_set() and self.running:
                # Check failsafe
                if self._check_failsafe():
                    self.running = False
                    break
                
                # Wait if paused
                self._pause_event.wait()
                
                # Check if it's time for the next action
                current_time = time.time()
                if current_time < next_action_time:
                    # Small sleep to reduce CPU usage
                    time.sleep(0.1)
                    continue
                
                try:
                    # Decide whether to move mouse or scroll
                    action_type = "scroll" if (self.enable_scrolling and random.random() < 0.3) else "move"
                    
                    if action_type == "scroll":
                        # Perform random scrolling
                        scroll_amount = random.randint(self.scroll_min_amount, self.scroll_max_amount)
                        logger.info(f"Scrolling with amount: {scroll_amount}")
                        if self._safe_scroll(scroll_amount):
                            self.status_update.emit(f"Scrolled with amount: {scroll_amount}")
                    else:
                        # Get random target position, staying away from edges
                        target_x = random.randint(50, screen_width - 50)
                        target_y = random.randint(50, screen_height - 50)
                        
                        # Get current position
                        current_x, current_y = pyautogui.position()
                        
                        # Move based on selected path
                        if self.movement_path == "straight":
                            duration = random.uniform(self.min_interval, self.max_interval)
                            logger.info(f"Moving straight to {target_x}, {target_y} over {duration:.2f}s")
                            if not self._safe_move(target_x, target_y, duration):
                                continue
                        
                        elif self.movement_path == "zigzag":
                            # Create a zigzag path
                            mid_x = (current_x + target_x) // 2
                            mid_y = (current_y + target_y) // 2
                            
                            logger.info(f"Moving zigzag from {current_x}, {current_y} to {target_x}, {target_y}")
                            
                            # First segment
                            if self._stop_event.is_set() or not self.running or self._check_failsafe():
                                break
                            self._pause_event.wait()
                            duration = random.uniform(self.min_interval/3, self.max_interval/3)
                            if not self._safe_move(mid_x, current_y, duration):
                                continue
                            
                            # Second segment
                            if self._stop_event.is_set() or not self.running or self._check_failsafe():
                                break
                            self._pause_event.wait()
                            duration = random.uniform(self.min_interval/3, self.max_interval/3)
                            if not self._safe_move(mid_x, mid_y, duration):
                                continue
                            
                            # Third segment
                            if self._stop_event.is_set() or not self.running or self._check_failsafe():
                                break
                            self._pause_event.wait()
                            duration = random.uniform(self.min_interval/3, self.max_interval/3)
                            if not self._safe_move(target_x, mid_y, duration):
                                continue
                            
                            # Final segment
                            if self._stop_event.is_set() or not self.running or self._check_failsafe():
                                break
                            self._pause_event.wait()
                            duration = random.uniform(self.min_interval/3, self.max_interval/3)
                            if not self._safe_move(target_x, target_y, duration):
                                continue
                        
                        else:  # random path
                            # Create random points for the path
                            num_points = random.randint(2, 5)
                            points = [(current_x, current_y)]
                            
                            for _ in range(num_points):
                                points.append((
                                    random.randint(min(current_x, target_x), max(current_x, target_x)),
                                    random.randint(min(current_y, target_y), max(current_y, target_y))
                                ))
                            
                            points.append((target_x, target_y))
                            
                            logger.info(f"Moving randomly through {len(points)} points from {current_x}, {current_y} to {target_x}, {target_y}")
                            
                            # Move through each point
                            segment_duration = random.uniform(self.min_interval, self.max_interval) / len(points)
                            for x, y in points[1:]:
                                if self._stop_event.is_set() or not self.running:
                                    break
                                self._pause_event.wait()
                                if self._check_failsafe():
                                    self.running = False
                                    return
                                if not self._safe_move(x, y, segment_duration):
                                    break
                        
                        # Perform click if specified and not none
                        if self.click_type != "none":
                            logger.info(f"Performing {self.click_type} click")
                            if not self._safe_click():
                                continue
                        
                        # Update status
                        self.status_update.emit(f"Mouse moved to {target_x}, {target_y}")
                    
                except pyautogui.PyAutoGUIException as e:
                    if not self._handle_error(e):
                        break
                except Exception as e:
                    if not self._handle_error(e):
                        break
                
                # Wait before next movement
                pause_time = random.uniform(self.between_min_interval, self.between_max_interval)
                logger.info(f"Pausing for {pause_time:.2f}s before next movement")
                
                # Set the time for the next action
                next_action_time = time.time() + pause_time
                
                # Use a loop with small steps to allow for quicker response to stop/pause
                start_time = time.time()
                while time.time() - start_time < pause_time:
                    if self._stop_event.is_set() or not self.running:
                        break
                    if self._check_failsafe():
                        self.running = False
                        return
                    time.sleep(0.1)
            
            self.status_update.emit("Mouse automation completed normally")
                
        except Exception as e:
            self.status_update.emit(f"Error in mouse automation: {str(e)}")
            logger.error(f"Unhandled error in mouse automation: {str(e)}")
            self.error_occurred.emit(f"Unhandled error in mouse automation: {str(e)}")
        finally:
            self.running = False


class KeyboardAutomation(AutomationBase):
    """Class to handle keyboard typing automation."""
    
    def __init__(self):
        super().__init__()
        # Default settings
        self.min_interval = 0.1
        self.max_interval = 0.3
        self.text_to_type = "The quick brown fox jumps over the lazy dog."
        self.randomize_typing = True
        self.pause_before_repeat = 2.0  # Seconds to wait before repeating the text
    
    def _check_failsafe(self):
        """Check if mouse is in a failsafe position (top-left corner)."""
        if not self.failsafe_active:
            return False
            
        try:
            x, y = pyautogui.position()
            if x < 5 and y < 5:  # If mouse in top-left corner
                self.status_update.emit("Failsafe triggered: Mouse in corner")
                self.failsafe_triggered.emit()
                return True
        except Exception as e:
            logger.warning(f"Error checking failsafe: {str(e)}")
        
        return False
    
    def _safe_type(self, char):
        """Safely type a character with error handling."""
        try:
            pyautogui.write(char)
            return True
        except pyautogui.PyAutoGUIException as e:
            return self._handle_error(e)
        except Exception as e:
            return self._handle_error(e)
    
    def _run(self):
        """Main loop for keyboard automation."""
        try:
            if not self.text_to_type:
                # Use a default text instead of stopping
                self.text_to_type = "The quick brown fox jumps over the lazy dog."
                self.status_update.emit("No text provided. Using default text.")
                
            self.status_update.emit("Keyboard automation started")
            retry_count = 0
            
            while not self._stop_event.is_set() and self.running:
                try:
                    # Type the text character by character
                    for char in self.text_to_type:
                        # Check if we should stop
                        if self._stop_event.is_set() or not self.running:
                            break
                        
                        # Check failsafe
                        if self._check_failsafe():
                            self.running = False
                            break
                        
                        # Wait if paused
                        self._pause_event.wait()
                        
                        # Type the character
                        logger.debug(f"Typing character: '{char}'")
                        if not self._safe_type(char):
                            retry_count += 1
                            if retry_count >= 3:
                                self.status_update.emit("Too many typing errors, pausing briefly")
                                time.sleep(1.0)
                                retry_count = 0
                            continue
                        
                        # Update status (don't flood with updates)
                        if random.random() < 0.1:  # Only update ~10% of the time
                            self.status_update.emit(f"Typed: {char}")
                        
                        # Wait random interval if randomized, or fixed interval
                        wait_time = 0
                        if self.randomize_typing:
                            wait_time = random.uniform(self.min_interval, self.max_interval)
                        else:
                            wait_time = self.min_interval
                        
                        # Break waiting into smaller chunks to check for stop/pause
                        wait_start = time.time()
                        while time.time() - wait_start < wait_time:
                            if self._stop_event.is_set() or not self.running:
                                break
                            if self._check_failsafe():
                                self.running = False
                                return
                            time.sleep(min(0.05, wait_time))  # Small sleep to reduce CPU usage
                    
                    # Text completed, update status
                    self.status_update.emit(f"Completed typing text ({len(self.text_to_type)} characters)")
                    
                    # Wait before repeating
                    logger.info(f"Waiting {self.pause_before_repeat} seconds before repeating text")
                    
                    # Break waiting into smaller chunks to check for stop/pause
                    wait_start = time.time()
                    while time.time() - wait_start < self.pause_before_repeat:
                        if self._stop_event.is_set() or not self.running:
                            break
                        if self._check_failsafe():
                            self.running = False
                            return
                        time.sleep(0.1)  # Small sleep to reduce CPU usage
                
                except pyautogui.PyAutoGUIException as e:
                    if not self._handle_error(e):
                        break
                except Exception as e:
                    if not self._handle_error(e):
                        break
            
            self.status_update.emit("Keyboard automation completed normally")
                
        except Exception as e:
            error_msg = f"Error in keyboard automation: {str(e)}"
            logger.error(error_msg)
            self.status_update.emit(error_msg)
            self.error_occurred.emit(error_msg)
        finally:
            self.running = False 