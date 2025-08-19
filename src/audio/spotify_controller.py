import os
import logging
from typing import Optional

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .base_audio_controller import BaseAudioController, PlaybackState

logger = logging.getLogger(__name__)

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
            logger.info("Spotify OAuth setup complete")
        except Exception as e:
            logger.exception("Failed to authenticate with Spotify")
            raise RuntimeError(f"Spotify setup failed: {e}")

    def play(self) -> None:
        """
        Starts playback if currently paused
        Updates internal playback state
        """
        self._change_playback_state(action = 'play', target_state = PlaybackState.PLAYING)

    def pause(self) -> None:
        """
        Pauses playback if currently paused
        Updates internal playback state
        """
        self._change_playback_state(action = 'pause', target_state = PlaybackState.PAUSED)

    def set_volume(self, volume_percent: int) -> None:
        """
        Sets the playback volume on the current device

        Args:
            volume_percent [int]: Volume level [0-100]
        """
        try:
            if not isinstance(volume_percent, int):
                logger.error("Volume level must be an integer, got %s", type(volume_percent))
                return
            if not (0 <= volume_percent <= 100):
                logger.error("Invalid volume percent: %s. Must be an integer between 0 and 100", volume_percent)
                return

            logger.debug("Attempting to set volume percent to %s", volume_percent)

            playback = self.spotify.current_playback()
            if not playback:
                logger.warning("No active playback detected, attempting to find active device...")
                devices = self.spotify.devices().get("devices", [])
                if not devices:
                    logger.error("No available device found.")
                    return
                active_device = next((d for d in devices if d.get("is_active")), devices[0])
                device_id = active_device.get("id")
                if not device_id:
                    logger.error("Could not determine a valid device ID.")
                    return
                logger.info("Using fallback device: %s", active_device.get("name", "Unknown"))
            else:
                device = playback.get("device")
                if not device:
                    logger.error("Playback found but no device info available")
                    return
                if not device.get("supports_volume", False):
                    logger.warning("Device '%s' does not support volume control", device.get("name", "unknown"))
                    return
                device_id = device.get("id")
                self.spotify.volume(volume_percent=volume_percent, device_id=device_id)
                logger.info("Volume successfully set to %s on device %s", volume_percent, device_id)

        except Exception as e:
            logger.exception("Unexpected error while setting volume: %s", str(e))

    def _change_playback_state(self, action: str, target_state: PlaybackState) -> None:
        """
        Generic method to change playback context state
        Args:
            action [str]: One of 'play' or 'pause'
            target_state [PlaybackState]: Enum representing the internal playback to set
        """
        try:
            logger.debug("Attempting to %s playback...", action)
            playback = self.spotify.current_playback()

            if not playback:
                logger.error("No playback detected; cannot %s", action)
                return

            is_playing = playback.get("is_playing", False)

            action_conditions = {
                "pause": is_playing,
                "play": not is_playing
            }

            if action not in action_conditions:
                logger.error("Invalid action: %s", action)

            if not action_conditions[action]:
                logger.debug("Playback already %sed; no action taken", action)
                return

            action_methods = {
                "pause": self.spotify.pause_playback,
                "play": self.spotify.start_playback
            }

            logger.debug("Executing '%s' playback action...", action)
            action_methods[action]()
            self._playback_context["state"] = target_state
            logger.debug("Playback successfully changed")

        except spotipy.SpotifyException as e:
            logging.error("Spotify API error while pausing playback: %e", e)
        except Exception as e:
            logging.error("Unexpected error while trying to pause playback: %e", e)


