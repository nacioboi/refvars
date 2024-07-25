from sys import path
import os
path.append(os.path.abspath(os.getcwd()))

import refvars


def get_command(args):
	print("Commands: ")
	for i in range(len(args)):
		print(f"{i+1}: {args[i]}")
	inp = ""
	while inp not in [str(i+1) for i in range(len(args))]:
		inp = input("Enter command idx: ").strip()
	return args[int(inp)-1]

def inst():
	with refvars.alloc_handler(address_book="ipc.ab") as (handler, mem):
		handler.allocate("x", mem.t.BOOL, eq=mem.FALSE)
		handler.allocate("exit_flag", mem.t.BOOL, eq=mem.FALSE)
		x = mem.get("x")
		exit_flag = mem.get("exit_flag")
		while exit_flag.read_bool() == False:
			print("\n\n\n\n\n")
			inp = get_command(["read", "flip", "shutdown", "spawn child"])
			if inp == "read":
				print(f"x: {str(x)}")
			elif inp == "flip":
				x.write_bool(not x.read_bool())
			elif inp == "shutdown":
				exit_flag.write_bool(True)
				break
			elif inp == "spawn child":
				# TODO: Groundwork is done but windows is killing us since we're trying to access memory from a process that is not the owner.
				# To fix this we have two options:
				# 1. Use MMF to share memory between processes, we have to work with the worst API in existence. (Windows)
				# Pros: Really, really fast. Also, uses less memory.
				# Cons: Windows API is a nightmare.
				# 2. Use a series of sockets to send updates from the owner of the memory to the appropriate process.
				# Pros: Cross-platform, easy to implement.
				# Cons: Slower than MMF, uses more memory.
				from multiprocessing import Process
				Process(target=inst, daemon=True).start()
				from time import sleep
				sleep(5)

		print("Shutting down...")
		from random import randint
		from time import sleep
		sleep(randint(1, 5))
		if exit_flag.read_bool() == True:
			# This program will call the shutdown since we were the first to reach this point.
			exit_flag.write_bool(False)
			handler.shutdown(verbose=True)
		print("Shutdown complete.")

if __name__ == "__main__":
	inst()
