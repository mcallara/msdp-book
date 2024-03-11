# TODO
# - Multiplication
# - Sum between currencies

# Next step: in the multiplication, 2 is the value of the multiplier. 
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    five.times(multiplier=2)
    assert 10 == five.amount
    
class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        self.amount = self.amount * 2

    

    