
Refactoring: Improving the Design of Existing Code - Martin Fowler
Design Principles and Design Patterns - Robert C. Martin
https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf
Clean Code - Robert C. Martin
Domain-Driven Design - Tackling Complexity in the Heart of Software - Eric Evans

Some concepts to start reading:
- Duck Typing in Python
- Runtime polymorphism (or method overriding) vs Static Polymorphism (method overloading or compile-time polymorphism)
- Value Objects
- Immutable Objects

Who invented TDD? Why Kent Beck refers to the rediscovery of TDD? What is the history of TDD before Kent Beck's rediscovery?
https://www.quora.com/Why-does-Kent-Beck-refer-to-the-rediscovery-of-test-driven-development-Whats-the-history-of-test-driven-development-before-Kent-Becks-rediscovery


# Note the duck typing

# Runtime polymorphism or method overriding, is the ability of a method to behave differently based on the object that calls it.

# Static Polymorphism (method overloading or compile-time polymorphism): multiple methods have the same name but differ in the type or number of their parameters.
# The decision about which method to call is made at compile time

At the moment, when we multiply a Dollar, the amount changes. This generates what we call a side-effect.

"Side effects can make code more difficult to reason about, since they introduce hidden dependencies and make it harder to understand how changes to one part of the code will affect the rest of the system."

So to avoid this side-effect, when we will multiply our dollar, we will return a new dollar as a result instead of modifying the original object.

"value object" is an object that represents a simple entity whose equality is not based on identity: i.e. two value objects are equal when they have the same value, not necessarily being the same object. 

Reference: Value Object is presented in "Domain-Driven Design - Tackling Complexity in the Heart of Software - Eric Evans" and is also a design pattern.

"immutable object" is an object whose state cannot be modified after it is created. This is in contrast to a mutable object, which can be modified after it is created.

Making Dollar an immutable object will help us avoid side-effects.