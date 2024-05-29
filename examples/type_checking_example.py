import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from refvars import new

#
# If you're editor supports, we can use type hints to help intellisense.
#

# Create a reference to a string.
ref = new[str]("Hello, World!").get_ref()  # Notice the type hint.

# Get the value of the reference.
print(ref.get())  # Hello, World!

