import os
from typing import Optional

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .base_audio_controller import BaseAudioController, PlaybackState

class SpotifyController(BaseAudioController):
    """
    A controller to interact with Spotify's Web API for audio playback management.
    Inherits from BaseAudioController and handles authentication, playback state, and controls commands
    """

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.client_id: Optional[str] = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret: Optional[str] = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri: Optional[str] = os.getenv("SPOTIPY_REDIRECT_URI")

        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing required environment variables for Spotify OAuth")

        self.scope: str = 'user-modify-playback-state user-read-playback-state'
        self.spotify: Optional[spotipy.Spotify] = None

    def setup(self) -> None:
        """
        Sets up the Spotipy client with OAuth authentication
        Raises:
            RuntimeError: If the Spotipy setup fails
        """
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

    def play(self) -> None:
        """
        Starts playback if currently paused
        Updates internal playback state
        """
        try:
            playback = self.spotify.current_playback()
            if playback and not playback.get('is_playing', False):
                self.spotify.start_playback(device_id = None)
                self._playback_state["state"] = PlaybackState.PLAYING
        except spotipy.SpotifyException as e:
            print(f"[Error] Failed to start playback: {e}")

    def pause(self) -> None:
        """
        Pauses playback if currently paused
        Updates internal playback state
        """
        try:
            playback = self.spotify.current_playback()
            if playback and playback.get('is_playing', False):
                self.spotify.pause_playback(device_id = None)
                self._playback_state["state"] = PlaybackState.PAUSED
        except spotipy.SpotifyException as e:
            print(f"[Error] Failed to pause playback: {e}")

    def set_volume(self, volume_level: int) -> None:
        """
        Sets the playback volume on the current device

        Args:
            volume_level [int]: Volume level [0-100]
        """
        pass