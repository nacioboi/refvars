import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from refvars import new, Reference

# Create a reference to a string.
ref = new[str]("Hello, World").get_ref()

# Get the value of the reference.
print(ref.get())  # `Hello, World`

# We can also use `ref.value` to get the value of the reference.
print(ref.value)  # `Hello, World`

# Change the value of the reference.
def add_to_the_end(value:"Reference[str]"):
    value.set(value.get() + "!")
add_to_the_end(ref)

# We can also use `ref.value += "!"` to change the value of the reference.
ref.value += "xXx "

# Confirm the value had changed.
print(ref.get()) # `Hello, World!xXx `

# All operators are supported using `ref.value`.
ref.value *= 2

print(ref.get())  # `Hello, World!xXx Hello, World!xXx`

# NOTE: REMEMBER:
# The `Reference.set` allows for runtime type checking, so we recommend using it.
