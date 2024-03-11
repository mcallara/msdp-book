# TODO
# - Multiplication
# - Sum between currencies

# Fixed the test! Let's refactor, by avoiding duplication.
# Next step: Let's make the duplication evident replacing 10 with 5 * 2.
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    five.times(multiplier=2)
    assert 10 == five.amount
    
class Dollar:
    def __init__(self, amount):
        pass
    
    def times(self, multiplier):
        pass

    amount = 10