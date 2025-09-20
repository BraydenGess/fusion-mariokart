import os
import time
import threading
from dotenv import load_dotenv

from .player.spotify_player import SpotifyPlayer

import logging
logger = logging.getLogger(__name__)

class AudioController(threading.Thread):
    def __init__(self, game_state, poll_interval: float = 0.05):
        super().__init__(daemon = True)
        self.game_state = game_state
        self.poll_interval = poll_interval
        self.last_state = None
        self.running = True

        self.audio_player = self._build_audio_player()

    def run(self):
        while self.running:
            state = self.game_state.get()
            if state != self.last_state:
                self._update_playback(state)
                self.last_state = state
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False
        self.join()
        logger.info("AudioController Stopped")

    def _update_playback(self, state):
        print('Updating playback')

    def _build_audio_player(self):

        load_dotenv()
        audio_sources = os.getenv("AUDIO_SOURCES").split(",")

        player_factory = {
            'Spotify': lambda: SpotifyPlayer()
        }

        for source in audio_sources:
            factory = player_factory.get(source)
            if not factory:
                logging.warning(f"Unknown source: {source}")
                continue

            try:
                player = factory()
                player.setup()
                logger.info(f"Using player {source}")
                return player
            except Exception as e:
                logger.warning(f"Failed to initialize player {source}: {e}")

        logger.error(f"Failed to build audio player")
        raise ValueError("Failed to build AudioPlayer")