import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .base_audio_controller import BaseAudioController, PlaybackState

class SpotifyController(BaseAudioController):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing required environment variables for Spotify OAuth")

        self.scope = 'user-modify-playback-state user-read-playback-state'

        self.spotify = None

    def setup(self):
        try:
            self.spotify = spotipy.Spotify(
                auth_manager = SpotifyOAuth(
                    client_id = self.client_id,
                    client_secret = self.client_secret,
                    redirect_uri = self.redirect_uri,
                    scope = self.scope,
                )
            )
        except Exception as e:
            raise RuntimeError(f"[Error] Spotify setup failed: {e}")

    def play(self):
        playback = self.spotify.current_playback()
        if playback and not playback['is_playing']:
            self.spotify.start_playback(device_id=None)
            self._playback_state["state"] = PlaybackState.PLAYING

    def pause(self):
        playback = self.spotify.current_playback()
        if playback and playback['is_playing']:
            self.spotify.pause_playback(device_id=None)
            self._playback_state["state"] = PlaybackState.PAUSED

    def set_volume(self, volume_level: int):
        pass