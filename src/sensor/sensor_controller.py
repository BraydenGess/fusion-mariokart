import threading
from .detector.random_detector import RandomDetector

import logging
logger = logging.getLogger(__name__)

class SensorController(threading.Thread):
    def __init__(self, game_state, poll_interval = 0.1):
        super().__init__(daemon = True)
        self.game_state = game_state
        self.poll_interval = poll_interval
        self.running = True

        self.detector = self._build_detector()

    def run(self):
        while self.running:
            new_state = self.detector.detect()
            self.game_state.update(status = new_state)

    def stop(self):
        self.running = False
        self.join()
        logger.info("SensorController Stopped")

    def _build_detector(self):
        return RandomDetector()