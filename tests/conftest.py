"""Shared test fixtures."""

import json
import os

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def load_fixture():
    """Return a helper that loads a JSON fixture by name."""

    def _load(name: str) -> dict:
        path = os.path.join(FIXTURES_DIR, f"{name}.json")
        with open(path) as f:
            return json.load(f)

    return _load
