from refvars import Make_Reference

#
# If you're editor supports, we can use type hints to help intellisense.
#

# Create a reference to a string.
ref = Make_Reference[str]("Hello, World!").reference  # Notice the type hint.

# Get the value of the reference.
print(ref.get())  # Hello, World!

