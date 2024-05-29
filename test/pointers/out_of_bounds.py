import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import alloc, Pointer

def out_of_bounds_callback(ptr:"Pointer") -> None:
	print(f"Address: {ptr.address}")
	more_than_64 = b"X" * 65
	ptr.write(more_than_64)
	
alloc(64).safe_access(out_of_bounds_callback)
