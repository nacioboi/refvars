import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import new

x = new[int](0).get_ref()

# NOTE: The below should raise a TypeError.
# NOTE:  This is intended behavior, hence the `#type:ignore` comment.
x.set(3.14) #type:ignore
