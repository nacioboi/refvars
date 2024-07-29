import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from refvars import new, Reference

def times_10(bar:"Reference[int]") -> "None":
	bar.value *= 10

my_ref = new[int](10).get_ref()
times_10(my_ref)
print(my_ref.value)
assert my_ref.value == 100

print("Success!")
