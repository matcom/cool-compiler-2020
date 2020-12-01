import os

import pytest


@pytest.fixture
def compiler_path():
    return os.path.abspath("./coolc.sh")
