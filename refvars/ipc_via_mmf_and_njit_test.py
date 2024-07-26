"""
This file will demonstrate how to use IPC via MMF (Memory Mapped Files) in Python.

This technique uses njit along with ctypes to create a fast and efficient IPC mechanism.

No more multiprocessing overhead, no more slow IPC.

===================

We will be using c to reverse 10,000,000 strings of a few characters each.

Luckily, RAM is insanely fast and we can easily handle this much data.
"""



import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
os.chdir(os.path.dirname(__file__))

import lib_mem
import python_to_c

from numba import njit
import numpy as np
import threading
import time



@njit(cache=True)
def request_giver(index:"int") -> "bytes":
	# This function will be called by the C service to get a request.
	# We will return a request here.
	if index == 0:
		l = []
		# Manual loops are faster than list comprehensions with njit.
		for _ in range(1000):
			l.append(b"a")
			l.append(b"b")
			l.append(b"c")
		l.append(b"\0")
		return b"".join(l)
	else:
		return b"\0"  # Signal to stop.



@njit(cache=True)
def result_receiver(ptr) -> "bool":
	# This function will be called by the C service to give the result.
	# We will receive the result here.
	result = python_to_c.decoder(ptr)  # Note we must decode the result.
	print(f"Result received: len=[{len(result)}]")
	print(f"First three characters: [{result[:3]}]")
	print(f"Last three characters: [{result[-3:]}]")
	return True



def main():
	# To start, we need to bootstrap the MMF service in native python.
	res = lib_mem.start_mmf_service(
		b"test", # Name of the MMF.
		1024,    # Size (lower 32bits) of the MMF.
		0        # Size (upper 32bits) of the MMF.
	)
	if res != 0:
		raise Exception("Failed to start MMF service.")
	print("Started MMF service.")

	ptr = lib_mem.get_mmf_ptr()
	if not os.path.exists("ptr.txt"):
		with open("ptr.txt", "w") as f:
			f.write(str(ptr))
	print("Got MMF pointer:", ptr)

	start_time = time.perf_counter()
	print(f"Start Time [{start_time}].")
	# In order for this to work, we actually have to do things kina reverse.
	# We will bootstrap the C service and then:
	#  - C will constantly ask for a request.
	#  - Python will decide what request (if any) to give.
	#  - Once C has a request, it will process it.
	#  - C will then give the result back to Python.
	# The C service will get the request from-
	python_to_c.Python_To_C(
		request_giver,    # The request giver function.
		result_receiver,  # And the result, from c, will be returned, to python, via the result receiver function.
	).start_service("./libservice.dll")

	# The `start_service` function will block until the `request_giver` function returns a signal to stop.
	# BTW, the signal to stop is a the first byte being b"\0".
	print("Stopped `Python_To_C` service.")
	res = lib_mem.stop_mmf_service()
	if res != 0:
		raise Exception("Failed to stop MMF service.")
	print("Stopped MMF service.")

	end_time = time.perf_counter()
	print(f"End Time [{end_time}].")
	print(f"Total Time [{end_time - start_time}].")

main()




