import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .base_audio_controller import BaseAudioController

class SpotifyController(BaseAudioController):
    def play(self):
        """Resumes playback if music is currently paused"""
        playback = self.spotify.current_playback()
        if playback and not playback['is_playing']:
            self.spotify.start_playback(device_id = None)