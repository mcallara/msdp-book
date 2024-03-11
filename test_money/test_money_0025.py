# TODO
# - Multiplication - DONE
# - Sum between currencies
# - Side effects of multiplication - DONE
# - Equality - DONE
# - Amount should be private - DONE
# - Support for Francs (support another currency) - DONE

# Next step: Move amount to Money
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

class Money:
    pass

class Dollar(Money):
    def __init__(self, amount):
        self._amount = amount
    
    def times(self, multiplier):
        return Dollar(self._amount * multiplier)

    def __eq__(self, dollar):
        return self._amount == dollar._amount

class Franc:
    def __init__(self, amount):
        self._amount = amount
    
    def times(self, multiplier):
        return Franc(self._amount * multiplier)

    def __eq__(self, franc):
        return self._amount == franc._amount

