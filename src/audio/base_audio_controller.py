from abc import ABC, abstractmethod

class BaseAudioController(ABC):

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