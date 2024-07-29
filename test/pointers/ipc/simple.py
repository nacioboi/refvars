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

def new_window(term):
	from subprocess import CREATE_NEW_CONSOLE, Popen
	from sys import executable
	cmd = f"{term} {executable} {__file__}"
	Popen(cmd, creationflags=CREATE_NEW_CONSOLE)

def inst():
	with refvars.alloc_handler(address_book="ipc.ab") as (handler, mem):
		handler.allocate("x", mem.t.BOOL, eq_=mem.FALSE)
		handler.allocate("exit_flag", mem.t.BOOL, eq_=mem.FALSE)
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
				exit_flag.write_bool(True)  # Shutdown other processes.
				break
			elif inp == "spawn child":
				print("Spawning child process...")
				# TODO: Groundwork is done but windows is killing us since we're trying to access memory from a process that is not the owner.
				# To fix this we can use MMF to share memory between processes, we have to work with he worst API in existence. (Windows)
				# Pros: Really, really fast. Also, uses less memory.
				# Cons: Windows API is a nightmare.
				from multiprocessing import Process
				Process(target=new_window, daemon=True, args=("C:\\Windows\\system32\\cmd.exe /k",)).start()

		print("Shutting down...")
		handler.shutdown(verbose=True)
		print("Shutdown complete.")

if __name__ == "__main__":
	inst()
