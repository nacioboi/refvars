# Python Reference Variables `refvars`

This repository contains but two simple but extremely useful Python class, `new` and `Reference`.

**ALSO:** [C Pointers in Python](#c-pointers-in-python).

This holy grail of simple python hacks, `refvars` provides a convenient way to work with references to objects.
It allows you to set and get the value of the reference using simple `get` and `set` methods.

## Usage

To use the `refvars` class, simply import it into your Python script:

```python
import refvars
```

Then use `new` to create a reference to an object:

```python
# Create a reference.
ref = refvars.new[int](0).get_ref()
```

**Note**: that `new` will run a variety of runtime checks to ensure that the reference is being used correctly.

* The way these checks work is by very basic checking of source code.
* This can lead to some problems when trying to open your source code file with `inspect` module.

To fix this:

```python
refvars.disable_runtime_usage_checks()
```

Now, you can use the `Reference` to `get` and `set` the value of the reference:

```python
# To ensure that the initial value does actually change.
print(ref.get())  # 0

# If we want a function to modify the reference, we can pass the reference to the function.
def modify_reference(ref:"refvars.Reference[int]"):
    ref.set(1)

modify_reference(ref)

print(ref.get())  # 1
```

## Installation

To install the `refvars`, use pip:

```bash
pip install refvars
```

## C Pointers in Python

Yes, you heard it right. You can use `refvars` to access memory created by C code in Python.

```python
from refvars import alloc
```

The `alloc` is much the same to the `new` class. But instead we use `safe_access(< your cb >)` to safely access the memory.

```python
from refvars import alloc, Pointer

def callback(ptr:"Pointer") -> None:
	print(f"Address: {ptr.address}")
	# We even have basic error handling to stop you from writing more than 64 bytes.
	more_than_64 = b"X" * 65
	ptr.write(more_than_64)  # This will raise an error.
	
# This allocates 64 bytes of memory.
# Your callback will be called with a `Pointer` object as the only argument.
# On function return, the memory will be freed.
# Meaning that we are (hopefully) safe from memory leaks and cyber attacks.
alloc(64).safe_access(callback)
```

A working version you can use is:

```python
from refvars import alloc, Pointer

def callback(ptr:"Pointer") -> None:
	print(f"Address: {ptr.address}")
	data = b"Hello, World!"
	ptr.write(data)
	print(ptr.read(len(data)))  # b"Hello, World!"

alloc(1024).safe_access(callback)
```

## Confirmed versions of Python

* [x] 3.11 - Works perfectly on the old version (before c pointer update).
* [x] 3.12 - Works perfectly.

## License

Covered under the GNU General Public License v2.0.
