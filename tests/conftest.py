import os
import tempfile
import pytest

from flaskr import create_app
from flaskr import nlp_model

os.chdir("..")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True})
    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="session", params=[r"instance/word2vec.model"])
def word2vec_model(request):
    return nlp_model.load_word2vec_model(request.param)


@pytest.fixture(scope="session", params=[(r"instance/say_words.txt", r"instance/init_say_words.txt")])
def say_words(word2vec_model, request):
    return nlp_model.load_say_words(word2vec_model, *request.param)


@pytest.fixture(scope="session", params=[r"instance/stop_words.txt"])
def stop_words(request):
    return nlp_model.load_stop_words(request.param)


@pytest.fixture(scope="session", params=[(r"instance/vocabulary.txt", r"instance/speck_model")])
def speck_model(request):
    return nlp_model.load_speck_model(*request.param)


@pytest.fixture(scope="session")
def sif_model(stop_words, word2vec_model):
    return nlp_model.load_sif_model(word2vec_model, stop_words)
