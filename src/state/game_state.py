import threading

class GameState:
    def __init__(self):
        self._lock = threading.Lock()
        self._state = {
            "course_name": "None"
        }

    def update(self, **kwargs):
        with self._lock:
            self._state.update(kwargs)

    def get(self, key = None):
        with self._lock:
            if key:
                return self._state.get(key)
            return self._state.copy()