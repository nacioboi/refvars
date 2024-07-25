from sys import path
import os
path.append(os.path.abspath(os.getcwd()))

import refvars

with refvars.alloc_handler() as (handler, mem):
	handler.allocate("myvar", mem.t.U_INT_8)
	mem.get("myvar").write_uint8(255)
	a = mem.get("myvar").read_uint8()
	print(a)
	handler.deallocate("myvar")

