import warnings
warnings.filterwarnings("ignore", module="urllib3")

import os
import sys
import time
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.logging_config import setup_logging
setup_logging()

from src.audio.spotify_controller import SpotifyController

def test_pause(controller: SpotifyController) -> bool:
    # Pause Playback
    print("\nPausing playback...")
    controller.pause()
    time.sleep(2)

    # Verify paused
    paused_playback = controller.spotify.current_playback()
    if paused_playback:
        return not paused_playback.get("is_playing")
    else:
        raise RuntimeError("No playback info after pause")

def test_play(controller: SpotifyController) -> bool:
    # Pause Playback
    print("\nResuming playback...")
    controller.play()
    time.sleep(2)

    # Verify paused
    paused_playback = controller.spotify.current_playback()
    if paused_playback:
        return paused_playback.get("is_playing")
    else:
        raise RuntimeError("No playback info after play")

def run_test(name, func, **kwargs):
    result = func(**kwargs)
    status = "\u2705" if result else "\u274C"
    print(f"{status} {name} {'Passed' if result else 'Failed'}")

def main():
    try:
        controller = SpotifyController()
        print("Initializing SpotifyController...")

        controller.setup()
        print("Spotify setup successful!")

        current_playback = controller.spotify.current_playback()
        if current_playback is None:
            raise RuntimeError("No active playback found")
        else:
            track = current_playback.get("item", {}).get("name", "Unknown track")
            is_playing = current_playback.get("is_playing", False)
            print(f"Currently playing: '{track}', Playing status: {is_playing}")

        run_test('Pause', test_pause, controller = controller)
        run_test('Play', test_play, controller = controller)

    except Exception as e:
        print("An error occurred during Spotify integration test:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()