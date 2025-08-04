from abc import ABC, abstractmethod
from enum import Enum, auto

class PlaybackState(Enum):
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()
    BUFFERING = auto()

class BaseAudioController(ABC):
    def __init__(self):
        self._playback_context = {
            "track_id": None,
            "state": PlaybackState.STOPPED,
            "progress_ms": None,
            "timestamp": None,
        }

    @abstractmethod
    def setup(self):
        """Initialize authentication and prepare controller"""
        pass

    @abstractmethod
    def play(self):
        """Start or resume playback."""
        pass

    @abstractmethod
    def pause(self):
        """Pause playback."""
        pass

    @abstractmethod
    def set_volume(self, volume_percent: int):
        """Set playback volume [0-100]"""
        pass