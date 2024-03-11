# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality - DONE
# - Amount should be private - DONE
# - Support for Francs (support another currency) - DONE
# - Compare Francs with Dollars - DONE
# - Dollar / Franc duplication - DONE

# Next step: Remove Dollar and Franc classes
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
    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return self._amount == other._amount and self._currency == other._currency

    def dollar(amount):
        return Money(amount,"USD")

    def franc(amount):
        return Money(amount,"CHF")
    
    def times(self, multiplier):
        return Money(self._amount * multiplier, self._currency)
    