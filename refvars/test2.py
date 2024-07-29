import lib_mem

res = lib_mem.start_mmf_service(b"test", 1024, 0)
if res != 0:
	raise Exception("Failed to start MMF service.")
print("Started MMF service.")

ptr = lib_mem.get_mmf_ptr()
with open("ptr.txt", "w") as f:
	f.write(str(ptr))
print("Got MMF pointer:", ptr)

data = b"Hello, world!"
lib_mem.write(ptr, data)

data = lib_mem._read(ptr, len(data))
print("Read data:", data)

res = lib_mem.stop_mmf_service()
if res != 0:
	raise Exception("Failed to stop MMF service.")
print("Stopped MMF service.")
