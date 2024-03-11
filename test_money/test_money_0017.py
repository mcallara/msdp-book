# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality

# Next step: Now we need to implement a general solution for equality
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    ten = five.times(multiplier=2)
    assert 10 == ten.amount
    fifteen = five.times(multiplier=3)
    assert 15 == fifteen.amount

def test_equality():
    assert Dollar(3) == Dollar(3)
    assert Dollar(3) != Dollar(4) 

class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        return Dollar(self.amount * multiplier)

    def __eq__(self, dollar):
        return True

