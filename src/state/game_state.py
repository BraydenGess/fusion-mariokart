from threading import Lock

class GameState:
    def __init__(self):
        self._lock = Lock()
        self._current_course = None

    def set_course(self, course_name: str):
        with self._lock:
            self._current_course = course_name