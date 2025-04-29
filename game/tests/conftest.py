import pytest
from main import create_game


@pytest.fixture
def game():
    return create_game()
