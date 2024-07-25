import lib_mem

lib_mem.set_debug(True)

res = lib_mem.start_mmf_service(b"test", 1024, 0)
if res != 0:
	raise Exception("Failed to start MMF service.")
print("Started MMF service.")

ptr = lib_mem.get_mmf_ptr()
with open("ptr.txt", "w") as f:
	f.write(str(ptr))
print("Got MMF pointer:", ptr)

data = b"Hello!"
lib_mem.write(ptr, data)

input("Press Enter to stop MMF service...")

data = lib_mem.read(ptr, len(b"Hello, world!"))
print("Read data:", data)

res = lib_mem.stop_mmf_service()
if res != 0:
	raise Exception("Failed to stop MMF service.")
print("Stopped MMF service.")
