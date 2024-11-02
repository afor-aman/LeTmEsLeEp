import pyautogui
import random
import string
import time
import threading
import sys

class HumanInteractionMimicker:
    def __init__(self):
        self.stop_event = threading.Event()
        self.typing_thread_stopped_event = threading.Event()  # To control typing
        self.supported_chars = string.ascii_letters + string.digits + " !@#$%^&*()_+-=[];,<>?"
        
    def random_typing_speed(self):
        """Randomize typing delay to keep it under 50 WPM."""
        return random.uniform(0.3, 0.8)  # Adjust to about 30-50 WPM

    def random_mouse_delay(self):
        """Randomize delay for mouse movements."""
        return random.uniform(0.5, 2.0)  # Increase delay between mouse actions

    def random_scroll_delay(self):
        """Randomize delay for mouse scrolling."""
        return random.uniform(0.5, 1.5)  # Delay after each scroll

    def random_tab_delay(self):
        """Randomize delay for tab switching."""
        return random.uniform(5, 15)  # Longer intervals between tab changes

    def generate_random_word(self):
        """Generate a random word with a length between 3 and 8 characters."""
        length = random.randint(3, 8)
        return ''.join(random.choices(self.supported_chars, k=length))

    def type_random_text(self):
        """Continuously type random text with delays to mimic human behavior."""
        try:
            while not self.stop_event.is_set():
                # Generate a random number of words (between 1 and 5)
                num_words = random.randint(1, 5)
                sentence = ' '.join(self.generate_random_word() for _ in range(num_words)) + ' '  # Add a space after the sentence
                
                for word in sentence.split():
                    if self.stop_event.is_set():
                        break
                    pyautogui.typewrite(word, interval=self.random_typing_speed())  # Type each word
                    time.sleep(random.uniform(0.5, 1.5))  # Delay between typing words
                
                # Delay between typing bursts to mimic a more realistic typing pattern
                time.sleep(random.uniform(2.0, 4.0))
        except Exception as e:
            print(f"Error in type_random_text: {e}")

    def random_mouse_movement(self):
        """Randomly move the mouse cursor around the screen with pauses."""
        try:
            while not self.stop_event.is_set():
                x = random.randint(0, pyautogui.size().width)
                y = random.randint(0, pyautogui.size().height)
                duration = random.uniform(1.0, 3.0)  # Human-like movement duration
                pyautogui.moveTo(x, y, duration=duration)
                time.sleep(self.random_mouse_delay())
        except Exception as e:
            print(f"Error in random_mouse_movement: {e}")

    def random_mouse_scroll(self):
        """Randomly scroll the mouse with pauses."""
        try:
            while not self.stop_event.is_set():
                scroll_amount = random.randint(-10, 10)  # Random scroll amount
                pyautogui.scroll(scroll_amount)
                time.sleep(self.random_scroll_delay())  # Delay after each scroll
        except Exception as e:
            print(f"Error in random_mouse_scroll: {e}")

    def random_tab_change(self):
        """Randomly change tabs with delays, stopping typing during the switch."""
        try:
            while not self.stop_event.is_set():
                # Stop typing by setting the stop_event flag
                self.typing_thread_stopped_event.set()  # Signal the typing thread to pause
                time.sleep(0.2)  # Brief pause before pressing tab
                pyautogui.keyDown('command')  # Press and hold command key
                pyautogui.press('tab')  # Press tab
                time.sleep(0.2)  # Pause after tab press
                pyautogui.keyUp('command')  # Release command key
                time.sleep(self.random_tab_delay())  # Delay between tab changes
                self.typing_thread_stopped_event.clear()  # Resume typing
        except Exception as e:
            print(f"Error in random_tab_change: {e}")

    def start_interactions(self):
        """Start all interaction threads in a specific order: typing, mouse, then tab change."""
        threads = []
        try:
            # Start typing thread first
            typing_thread = threading.Thread(target=self.type_random_text)
            typing_thread.daemon = True
            typing_thread.start()  # Start the typing thread

            # Allow some time for the typing thread to start properly
            time.sleep(2)  # Optional: adjust as needed for smooth execution

            # Start mouse movement thread second
            mouse_movement_thread = threading.Thread(target=self.random_mouse_movement)
            mouse_movement_thread.daemon = True
            mouse_movement_thread.start()  # Start the mouse movement thread

            # Start mouse scroll thread third
            mouse_scroll_thread = threading.Thread(target=self.random_mouse_scroll)
            mouse_scroll_thread.daemon = True
            mouse_scroll_thread.start()  # Start the mouse scroll thread

            # Allow some time for the scroll thread to start properly
            time.sleep(2)  # Optional: adjust as needed for smooth execution

            # Start tab change thread last
            tab_change_thread = threading.Thread(target=self.random_tab_change)
            tab_change_thread.daemon = True
            tab_change_thread.start()  # Start the tab change thread

            # Keep track of all threads
            threads.append(typing_thread)
            threads.append(mouse_movement_thread)
            threads.append(mouse_scroll_thread)
            threads.append(tab_change_thread)

            # Wait until stop_event is set, keeping the main thread alive
            while not self.stop_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Stopping interactions...")
            self.stop_event.set()
        except Exception as e:
            print(f"Error in start_interactions: {e}")
        finally:
            # Ensure all threads are terminated gracefully
            self.stop_event.set()
            for thread in threads:
                if thread.is_alive():
                    thread.join()

if __name__ == "__main__":
    try:
        print("Starting human interaction mimicking script...")
        print("Press Ctrl+C to stop.")
        mimicker = HumanInteractionMimicker()
        mimicker.start_interactions()
    except Exception as e:
        print(f"Unhandled error: {e}")
        sys.exit(1)
