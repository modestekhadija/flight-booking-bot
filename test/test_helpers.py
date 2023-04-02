def increment(x):
    return x + 1

def decrement(x):
    return x - 1

def test_increment():
    assert increment(3) == 4

# This test is designed to fail for demonstration purposes.
def test_decrement():
    assert decrement(3) == 0