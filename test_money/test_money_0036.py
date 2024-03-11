# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality - DONE
# - Amount should be private - DONE
# - Support for Francs (support another currency) - DONE
# - Compare Francs with Dollars - DONE
# - Dollar / Franc duplication

# Next step: Use new dollar factory method in the tests
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Dollar(amount=5)
    assert Dollar(amount=10) == five.times(multiplier=2)
    assert Dollar(amount=15) == five.times(multiplier=3)

def test_franc_multiplication():
    # test that you can multiply a Franc by a number and get the right amount.
    five = Franc(amount=5)
    assert Franc(amount=10) == five.times(multiplier=2)
    assert Franc(amount=15) == five.times(multiplier=3)

def test_equality():
    assert Dollar(3) == Dollar(3)
    assert Dollar(3) != Dollar(4)
    assert Franc(3) == Franc(3)
    assert Franc(3) != Franc(4)
    assert Dollar(5) != Franc(5)

class Money:
    def __init__(self, amount):
        self._amount = amount

    def __eq__(self, other):
        return self._amount == other._amount and type(self) == type(other)

    def dollar(amount):
        return Dollar(amount)
    
class Dollar(Money):
    def times(self, multiplier):
        return Dollar(self._amount * multiplier)

class Franc(Money):   
    def times(self, multiplier):
        return Franc(self._amount * multiplier)

