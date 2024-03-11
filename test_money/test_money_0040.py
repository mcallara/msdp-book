# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality - DONE
# - Amount should be private - DONE
# - Support for Francs (support another currency) - DONE
# - Compare Francs with Dollars - DONE
# - Dollar / Franc duplication

# Next step: Fix the test adding currency to the classes
def test_multiplication():
    # test that you can multiply a Dollar by a number and get the right amount.
    five = Money.dollar(amount=5)
    assert Money.dollar(amount=10) == five.times(multiplier=2)
    assert Money.dollar(amount=15) == five.times(multiplier=3)

def test_franc_multiplication():
    # test that you can multiply a Franc by a number and get the right amount.
    five = Money.franc(amount=5)
    assert Money.franc(amount=10) == five.times(multiplier=2)
    assert Money.franc(amount=15) == five.times(multiplier=3)

def test_equality():
    assert Money.dollar(3) == Money.dollar(3)
    assert Money.dollar(3) != Money.dollar(4)
    assert Money.franc(3) == Money.franc(3)
    assert Money.franc(3) != Money.franc(4)
    assert Money.dollar(5) != Money.franc(5)

def test_currency():
    assert "USD" == Money.dollar(1)._currency
    assert "CHF" == Money.franc(1)._currency

class Money:
    def __init__(self, amount):
        self._amount = amount

    def __eq__(self, other):
        return self._amount == other._amount and type(self) == type(other)

    def dollar(amount):
        return Dollar(amount)

    def franc(amount):
        return Franc(amount)
    
class Dollar(Money):
    def times(self, multiplier):
        return Dollar(self._amount * multiplier)

class Franc(Money):   
    def times(self, multiplier):
        return Franc(self._amount * multiplier)

