# If you're editor supports, we can use type hints to help intellisense.

from refvars import Reference

# Create a reference to a string.
ref = Reference[str]("Hello, World!")  # Notice the type hint.

# Get the value of the reference.
print(ref())  # Hello, World!

