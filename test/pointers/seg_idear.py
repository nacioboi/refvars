from sys import path
import os
path.append(os.path.abspath(os.getcwd()))

import refvars

def handle_print(handler:"refvars.alloc_handler", mem:"refvars.Memory_Wrapper"):
	print_flag = mem.get("print_flag")
	buffer = mem.get("buffer")
	if print_flag.read_bool() == False:
		return
	print(buffer.read_str().decode(), end="", flush=True)
	print_flag.write_bool(False)

def worker(handler:"refvars.alloc_handler", mem:"refvars.Memory_Wrapper"):
	from time import sleep
	from random import randint
	from random import choice
	from string import ascii_letters
	lock = mem.get("lock")
	print_flag = mem.get("print_flag")
	buffer = mem.get("buffer")
	exit_flag = mem.get("exit_flag")
	while exit_flag.read_bool() == False:
		text = "".join(choice(ascii_letters) for _ in range(10)) + "\n"
		sleep(randint(1, 5)/10)
		while lock.read_bool() == True:
			if exit_flag.read_bool() == True:
				return
		lock.write_bool(True)
		buffer.write_str(text)
		print_flag.write_bool(True)
		while print_flag.read_bool() == True:
			if exit_flag.read_bool() == True:
				return
		lock.write_bool(False)

with refvars.alloc_handler() as (handler, mem):
	handler.allocate("print_flag", mem.t.BOOL, eq_=mem.FALSE)
	handler.allocate("lock", mem.t.BOOL, eq_=mem.FALSE)
	handler.allocate("buffer", mem.t.CHAR, mem.t.PTR, ptr_size_=1024)
	handler.allocate("exit_flag", mem.t.BOOL, eq_=mem.FALSE)

	# Simple test writes.
	mem.get("print_flag").write_bool(True)        ; assert str(mem.get("print_flag")) == str(mem.TRUE)
	mem.get("print_flag").write_bool(False)       ; assert str(mem.get("print_flag")) == str(mem.FALSE)
	mem.get("lock").write_bool(True)              ; assert str(mem.get("lock")) == str(mem.TRUE)
	mem.get("lock").write_bool(False)             ; assert str(mem.get("lock")) == str(mem.FALSE)
	mem.get("buffer").write_str("Hello, World!")  ; assert str(mem.get("buffer")) == "Hello, World!"
	mem.get("buffer").clear_str()                 ; assert str(mem.get("buffer")) == ""
	mem.get("buffer").write_str("Hello")          ; assert str(mem.get("buffer")) == "Hello"
	x = mem.get("buffer")
	x.write_str(str(x) + ", World!")              ; assert str(mem.get("buffer")) == "Hello, World!"

	from threading import Thread
	p1 = Thread(target=worker, args=(handler, mem))
	p2 = Thread(target=worker, args=(handler, mem))
	p1.start()
	p2.start()

	handler.out_hook("print_flag", "hook1", handle_print)
	from time import sleep
	sleep(3)
	handler.unhook("print_flag", "hook1")
	mem.get("exit_flag").write_bool(True)
	p1.join()
	p2.join()
	handler.shutdown(verbose=True)


