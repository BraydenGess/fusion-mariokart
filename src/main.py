import time
from config.logging_config import setup_logging
from state.game_state import GameState
from audio.audio_controller import AudioController
from sensor.sensor_controller import SensorController

class GameEngine:
    """Main orchestrator for game sensors and components"""
    def __init__(self):
        self.game_state = GameState()

        self.audio_controller = AudioController(self.game_state)
        self.sensor_controller = SensorController(self.game_state)

        self.threads = [self.audio_controller, self.sensor_controller]

    def start(self):
        """Starts all threads"""
        for thread in self.threads:
            thread.start()

    def stop(self):
        """Stops all threads gracefully"""
        for thread in self.threads:
            thread.stop()

    def run(self):
        """Main loop"""
        self.start()
        print(f"Application running. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"Exiting...")
            self.stop()

if __name__ == "__main__":
    setup_logging()
    GameEngine().run()