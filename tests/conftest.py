import pytest
import os

@pytest.fixture
def compiler_path():
	return os.path.abspath('./coolc.sh')