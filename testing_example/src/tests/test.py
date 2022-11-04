import pytest
from add import add


# Most similar to cargo test
class TestAdd:
    def test_add(self):
        assert add(1, 2) == 3
        assert add(2, 2) == 4

    def test_faulty_add(self):
        assert add(1, 2) == 3
        assert add(2, 2) == 5
