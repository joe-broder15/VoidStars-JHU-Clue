"""
the following is an example of unit tests using pytest.

pytest is a really sweet testing framework as it HAS NO OVERHEAD WHATSOEVER!
you just write up basic python, make your asserts, and then run pytest from the 
command line.
"""

# tests are literally just functions
def test_1():
    one = 1
    assert one == 1 #we just use asserts 

def test_2():
    # create a list of the first 200 even numbers
    l = [2*i for i in range(1,101)]

    # make sure they're correct
    for i in range(0,100):
        assert 2*(i+1) == l[i]

def not_a_test():
    assert True