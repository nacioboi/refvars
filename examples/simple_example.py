from refvars import Make_Reference

# Create a reference to a string.
ref = Make_Reference[str]("Hello, World!").reference

# Get the value of the reference.
print(ref.get()) # Hello, World!
