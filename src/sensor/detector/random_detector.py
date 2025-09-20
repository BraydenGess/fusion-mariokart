import random
import time

class RandomDetector:
    def __init__(self):
        pass

    def detect(self):
        # Randomly choose a state (simulating detection)
        action = random.choice(["IDLE", "RUNNING", "JUMPING"])
        new_state = {'course_name': action}
        time.sleep(random.uniform(0.5, 2))
        return new_state