import pytest
from pyls import main

@pytest.mark.parametrize("status",[(True),])
def test_pyls(status):
    out = main()
    assert out == status

def run_test():
    TEST_PATH = './test_pyls.py'
    exit_code = pytest.main([TEST_PATH, '-x', '--verbose', '-s', '--durations=100'])
    return exit_code
if __name__ == '__main__':
    run_test()