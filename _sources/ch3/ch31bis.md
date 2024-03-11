---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---

```{code-cell} bash
:tags: [remove-input]
cd ../home
mkdir ch3
cd ch3
```

% ## Kind of testing. Levels of Testing.
% ## Unit and Integration Testing.
% ## We test behaviors.
% ## Basic Test with Pytest
% ## Testing and Visual Studio Code 

# 3.1 Testing

What is a test?  “a procedure leading to acceptance or rejection.” 
What are tests useful for?
- To ensure that your code works as expected.
- To understand how the code works.
- To understand how the code should work.

Let's see this in action. To start as lightweigth as possbile, we will use doctest.

What is doctest? 
Doctest is a module that comes with Python and allows you to write tests in the docstrings of your code. 

Imagine that you are working on a Python file named `addition.py` and you developed the following  `add` function that adds two numbers and returns the result:

```{code-block} python
def add(a, b):
    return a + b
```

To ensure that everyone understands what the function is supposed to do, you went ahead and added a docstring to the function:

```{code-block} python
def add(a, b):
    """Compute the sum of two numbers."""
    return a + b
```

To ensure that the function works as expected and since you know that a usage example always makes the documentation much more clear, you decide to add a test in the docstring.

```{code-block} python
def add(a, b):
    """Compute the sum of two numbers.

    Usage example:
    >>> add(4.0, 2.0)
    6.0
    """
    return a + b
```

The added `doctest` has two parts:
- The first part is the test itself, it starts with `>>>` and contains the function call.
- The second part is the expected output, it is the expected result of the function call. 

```{code-cell} bash
:tags: ["remove-input","remove-output"]
echo $'def add(a, b):
    """Compute the sum of two numbers.

    Usage example:
    >>> add(4.0, 2.0)
    6.0
    """
    return a + b' > addition.py
```

Now to run the tests, you can use the following command in the terminal:

```{code-cell} bash
python -m doctest -v addition.py
```

```{admonition} What to notice
:class: hint
- Doctest automatillcally detected the test in the docstring and ran it.
- It shows the expected output and if the test passed.
```

We can add as many tests as we want to the docstring. For example, we can add a test for the case when the two numbers are integers:

```{code-block} python
def add(a, b):
    """Compute the sum of two numbers.

    Usage examples:
    >>> add(4.0, 2.0)
    6.0
    >>> add(1, 3)
    4
    """
    return a + b
```