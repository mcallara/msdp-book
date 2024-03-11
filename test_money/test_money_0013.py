# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication

# Next step: With the right test, now let's fix it by creating a new Dollar object with the new amount.
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    ten = five.times(multiplier=2)
    assert 10 == ten.amount
    fifteen = five.times(multiplier=3)
    assert 15 == fifteen.amount
    
class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        self.amount *= multiplier
