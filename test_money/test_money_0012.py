# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication

# We want the times method to return a new Dollar object with the new amount instead 
# of modifying the current object.
# Next step: No way to fix the test. We need to modify the test to reflect the new behaviour.
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    five.times(multiplier=2)
    assert 10 == five.amount
    five.times(multiplier=3)
    assert 15 == five.amount
    
class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        self.amount *= multiplier
