# Python Reference

This repository contains but one simple but extremely useful Python class, `Reference`.

This holy grail of classes, `Reference`, provides a convenient way to work with references to objects. It allows you to set and get the value of the reference using simple methods.

## Usage

To use the `Reference` class, simply import it into your Python script:

```python
from reference import Reference

# Create a reference
ref = Reference[int](0)

# If we want a function to modify the reference, we can pass the reference to the function.
def modify_reference(ref: Reference[int]):
    ref.set(1)

modify_reference(ref)

# Now the getting is a bit different.
print(ref()) # 1
```

## Installation

To install the `Reference` class, use pip:

```bash
pip install python-reference
```

## Confirmed versions of Python

- [x] 3.11 - Works perfectly.
- [ ] 3.12 - Not tested.

## License

Covered under the GNU General Public License v2.0.
