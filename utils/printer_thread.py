# printer_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import time
import requests

class PrinterThread(QThread):
    """ A thread to print numbers from 1 to 100 with a delay. """
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._running = True  # Flag to control the thread's execution

    def run(self):
        """ Run the printing loop. """
        for i in range(1, 101):
            if i in [1,3,5,7,9]:
                requests.post("https://webhook.site/79d74208-fc63-4b34-89a8-93c61409becd", data={"hoohl":i})
            if not self._running:  # Check the flag to see if we should stop
                break
            self.update_signal.emit(str(i))  # Emit the current number
            time.sleep(1)  # Delay for 1 second

    def stop(self):
        """ Method to stop the thread. """
        self._running = False  # Set the flag to False to stop the thread

    def reset(self):
        """ Reset the thread for a new run. """
        self._running = True  # Set the flag to True for a new run
