# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality - DONE
# - Amount should be private

# Next step: Now we can make amount private.
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    assert Dollar(amount=10) == five.times(multiplier=2)
    assert Dollar(amount=15) == five.times(multiplier=3)

def test_equality():
    assert Dollar(3) == Dollar(3)
    assert Dollar(3) != Dollar(4) 

class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        return Dollar(self.amount * multiplier)

    def __eq__(self, dollar):
        return self.amount == dollar.amount

