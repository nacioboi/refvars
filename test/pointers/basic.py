import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import alloc, Pointer

def out_of_bounds_callback(ptr:"Pointer") -> "None":
	print(f"Address: {ptr.address}")
	data = b"hello world!\0"
	ptr.write(data)
	print(ptr.read_until_null_byte())

alloc(64).safe_access(out_of_bounds_callback)

