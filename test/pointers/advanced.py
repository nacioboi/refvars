# Lets write an actual useful program that uses pointers.
# IPC.
# First arg: memory address as command line argument.
# Second arg: size of memory block.
# Third arg: number of primes to generate.
# It will put the resulting primes in the memory address.

import sys, os
if not sys.platform == "win32":
	raise NotImplementedError("This program is only implemented for Windows.")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import alloc, new, Pointer, Reference

from typing import Generator

def run_command_live(command, cancel_flag:"Reference[bool]") -> Generator[str,None,None]:
	process = os.popen(command)
	while True:
		if cancel_flag.get() == True:
			break
		line = process.readline()
		if not line:
			break
		yield line
	process.close()


def out_of_bounds_callback(ptr: "Pointer") -> None:
	c_program_path = os.path.abspath(os.path.join(BASE_DIR, "primes.exe"))
	n_primes = int(input("Enter the number of primes to generate: "))
	command = f"cmd.exe /k '{c_program_path}' {str(ptr.address)} {str(ptr.size)} {str(n_primes)}"
	
	stop_flag = new[bool](False).get_ref()

	for line in run_command_live(command, stop_flag):
		print(line, end="")

alloc(10240).safe_access(out_of_bounds_callback)  # 10 KB.
