"""
This file will demonstrate how to use IPC via MMF (Memory Mapped Files) in Python.
This technique uses njit along with ctypes to create a fast and efficient IPC mechanism.
No more multiprocessing overhead, no more slow IPC.

===================

We will be using c to reverse strings of a few characters each.
"""

# TODO: Make this process faster. RN its a nice proof of concept.
# TODO: In order to make it faster, we must ensure that we are only passing pointers and not copying the entire buffer.

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
os.chdir(os.path.dirname(__file__))

import refvars.ptc as ptc

from numba import njit
import time

#region bs
#@njit(cache=False, fastmath=True)
#def test_speed(size=1024):
#	for _ in range(size):
#		x = alloc(1024) # Changing this will not affect the performance.
#		# However, repeating this iteration will increase drastically decrease the performance.
#		# TODO: For this reason, we should add a Queue, to both python and c.
#		# TODO: We could even abstract away and cheat a little with the `alloc_handler` by squeezing many requests into one buffer.
#		p = x.unsafe_access(ALLOCATION_TYPE.UINT8)
#		p.write(b"\x01")
#		p.free()

#@njit(cache=False, fastmath=True)
#def test_allocation():
#	x = alloc(1)
#	p = x.unsafe_access(ALLOCATION_TYPE.UINT8, debug_=True)
#	p.free()

#print("Compiling...")
#@njit(cache=False, fastmath=True)
#def compile_all():
#	x = alloc(32)
#	p = x.unsafe_access(ALLOCATION_TYPE.UINT8)
#	p.spread(b"\x00")
#	p.write(b"\x01")
#	p.read()
#	p.free()
#compile_all()

#print("Testing allocation...")
#test_allocation()

#print("Testing Read/Write...")
#x = alloc(1024)
#p = x.unsafe_access(ALLOCATION_TYPE.UINT8)
#p.spread(b"\x00", True)
#p.write(b"\x01", True)
#res, data = p.read(True)
#print(f"Data: [{data}]")
#if data != b"\x01":
#	p.free()
#	raise Exception("Failed to read/write.")
#p.free()

# TODO: `safe_access` is not yet working.
#@njit(cache=False, fastmath=True)
#def _test_safe_access(p:"Pointer"):
#	p.write(b"\x01")
#	if p.read() != b"\x01":
#		p.free()
#		raise Exception("Failed to read/write.")
#	p.free()
#@njit(cache=False, fastmath=True)
#def test_safe_access():
#	alloc(1024).safe_access(ALLOCATION_TYPE.UINT8, _test_safe_access)
#
#print("Testing safe access...")
#test_safe_access()

#print("Testing speed...")
#from timeit import timeit
#print("Benchmarking...")
#print(f"BENCHMARK: Took [{timeit(test_speed, number=3)}] to allocate, set, and free 1KB of memory.")

#endregion



@njit(cache=True, fastmath=True)
def request_giver(index:"int", size:"int") -> "tuple[list[int],bool]":
	# This function will be called by the C service to get a request.
	# Returns:
	# - A list of integers, which will be the request.
	# - A boolean, which will False if we wish to stop the service.
	if index == 0:
		l:"list[str]" = []
		for _ in range(0, size-4, 4):
			l.append("a")
			l.append("b")
			l.append("c")
			l.append(" ")
		x:"list[int]" = []
		for b in l:
			x.append(ord(b))
		return x, True
	else:
		return [0], False
	
def request_giver_python(size:"int") -> "list[int]":
	l:"list[str]" = []
	for _ in range(0, size-4, 4):
		l.append("a")
		l.append("b")
		l.append("c")
		l.append(" ")
	x:"list[int]" = []
	for b in l:
		x.append(ord(b))
	return x



def reverse_string(s:"str") -> "str":
	return s[::-1]



@njit(cache=True, fastmath=True)
def result_receiver(result:"str") -> "bool":
	# This function will be called by the C service to give the result.
	# We will receive the result here.
	#print(f"Result received: len=[{len(result)}]")
	#print(f"First three characters: [{result[:3]}]")
	#print(f"Last three characters: [{result[-3:]}]")
	return True



def benchmark_python(size):
	start_time = time.perf_counter()
	for _ in range(75):
		req = request_giver_python(size)
		res = reverse_string("".join([chr(x) for x in req]))
		print(len(res), end=", ")
	end_time = time.perf_counter()
	print(f"Start Time [{start_time}].")
	print(f"End Time [{end_time}].")
	print(f"Total Time [{end_time - start_time}].")


def main():
	BUFF_SIZE = 8192*512

	# In order for this to work, we actually have to do things kina reverse.
	# We will bootstrap the C service and then:
	#  - C will constantly ask for a request.
	#  - Python will decide what request (if any) to give.
	#  - Once C has a request, it will process it.
	#  - C will then give the result back to Python.
	# The C service will get the request from-
	# NOTE: We must be in the correct directory for this to work.
	try:
		os.chdir("build")
		start_time = time.perf_counter()
		x = ptc.Python_To_C(
			request_giver,    # The request giver function.
			result_receiver,  # And the result, from c, will be returned, to python, via the result receiver function.
		)
		x.bootstrap_service("service.dll")
		mid_time = time.perf_counter()
		x.start_service(BUFF_SIZE)

		# The `start_service` function will block until the `request_giver` function returns a signal to stop.
		# BTW, the signal to stop is a the first byte being b"\0".
		end_time = time.perf_counter()
		print(f"Start Time [{start_time}].")
		print(f"Mid Time [{mid_time}].")
		print(f"End Time [{end_time}].")
		print(f"Total Time [{end_time - start_time}].")

		print("\n\n\n\n")
		print("Benchmarking Python:")
		benchmark_python(BUFF_SIZE)
	finally:
		os.chdir("..")

main()




