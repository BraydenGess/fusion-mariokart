import os
import pytest
from unittest import mock
from audio.spotify_controller import SpotifyController

# Helper: set required env variables
def set_spotify_env():
    os.environ["SPOTIPY_CLIENT_ID"] = "dummy_id"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "dummy_secret"
    os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"

def unset_spotify_env():
    os.environ.pop("SPOTIPY_CLIENT_ID", None)
    os.environ.pop("SPOTIPY_CLIENT_SECRET", None)
    os.environ.pop("SPOTIPY_REDIRECT_URI", None)

def test_init_with_valid_env(monkeypatch):
    set_spotify_env()
    controller = SpotifyController()
    assert controller.client_id == "dummy_id"
    assert controller.client_secret == "dummy_secret"
    assert controller.redirect_uri == "http://localhost:8080"
    assert controller.spotify is None
    unset_spotify_env()

@mock.patch("audio.spotify_controller.load_dotenv", lambda: None)
@mock.patch.dict(os.environ, {}, clear=True)
def test_init_missing_env(monkeypatch):
    unset_spotify_env()
    with pytest.raises(ValueError, match="Missing required environment variables for Spotify OAuth"):
        SpotifyController()

@mock.patch("audio.spotify_controller.SpotifyOAuth")
@mock.patch("audio.spotify_controller.spotipy.Spotify")
def test_setup_success(mock_spotify, mock_auth):
    set_spotify_env()
    controller = SpotifyController()
    controller.setup()
    mock_auth.assert_called_once()
    mock_spotify.assert_called_once()
    assert controller.spotify is not None
    unset_spotify_env()

@mock.patch("audio.spotify_controller.SpotifyOAuth", side_effect=Exception("OAuth failed"))
def test_setup_failure(mock_auth):
    set_spotify_env()
    controller = SpotifyController()
    with pytest.raises(RuntimeError, match="Spotify setup failed"):
        controller.setup()
    unset_spotify_env()

def test_play():
    controller = SpotifyController()
    assert hasattr(controller, "play")
    assert callable(controller.play)

def test_pause():
    controller = SpotifyController()
    assert hasattr(controller, "pause")
    assert callable(controller.pause)

def test_set_volume():
    controller = SpotifyController()
    assert hasattr(controller, "set_volume")
    controller.set_volume(50)


