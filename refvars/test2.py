import numpy as np

import lib_mem
import il2bl

res = lib_mem.start_mmf_service(True, b"test", 1024, 0)
if res != 0:
	raise Exception("Failed to start MMF service.")
print("Started MMF service.")

with open("ptr.txt", "r") as f:
	ptr = int(f.read())
print("Got MMF pointer:", ptr)

data = b"Hello, world!"
lib_mem.write(True, ptr,
	il2bl.ilist_to_blist(
		np.array(data, dtype=np.uint8)
	)
)

data = lib_mem.read(True, ptr, len(data))
print("Read data:", data)

res = lib_mem.stop_mmf_service(True)
if res != 0:
	raise Exception("Failed to stop MMF service.")
print("Stopped MMF service.")
