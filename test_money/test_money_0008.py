# TODO
# - Multiplication
# - Sum between currencies

# Next step: amount should be coming from the value passed to the constructor.
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    five.times(multiplier=2)
    assert 10 == five.amount
    
class Dollar:
    def __init__(self, amount):
        pass
    
    def times(self, multiplier):
        self.amount = 5 * 2

    

    