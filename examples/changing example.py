from refvars import Make_Reference, Reference_Instance

# Create a reference to a string.
ref = Make_Reference[str]("Hello, World!").reference

# Get the value of the reference.
print(ref.get()) # Hello, World!

# Change the value of the reference
def add_x_to_the_end(value:"Reference_Instance[str]"):
    value.set(value.get() + "xXx")
add_x_to_the_end(ref)

# Confirm the value had changed.
print(ref.get()) # Hello, World!xXx
