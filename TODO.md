# TODO for the `python_reference` repository

- [ ] Add the option for runtime type checking.
- [ ] Think of more features or just ways to improve.

## Known issues.

Take the following code:

```python
ref = Make_Reference("Hello, World!").reference
```

This will raise an error:

```text
Traceback (most recent call last):
  File "/Users/joel-watson/Documents/Programming-Projects/All/refvars/examples/simple_example.py", line 4, in <module>
    ref = Make_Reference("Hello, World!").reference
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/refvars/__init__.py", line 80, in __init__
    self._validate()
  File "/opt/homebrew/lib/python3.11/site-packages/refvars/__init__.py", line 60, in _validate
    caller = stack[3]
             ~~~~~^^^
IndexError: list index out of range
```

It requires the type hint to be there.

To correct the error:

```python
ref = Make_Reference[str]("Hello, World!").reference
```

### Solution

We need to implement custom error handling for this so the user knows what's up.
