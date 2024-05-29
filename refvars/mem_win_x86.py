import ctypes as _ctypes
from typing import Callable as _Callable
from os.path import abspath, exists, join, dirname

DLL_NAME = "mem_win_x86_lib.dll"
BASE_DIR = dirname(__file__)
DLL_PATH = abspath(join(BASE_DIR, DLL_NAME))

if not exists(DLL_PATH):
	raise FileNotFoundError(f"[{DLL_PATH}] not found in the same directory as this script.")



__lib = _ctypes.CDLL(DLL_PATH)

__CALLBACK_TYPE = _ctypes.CFUNCTYPE(None, _ctypes.c_void_p)

__safe_mem_acc = __lib.safe_memory_access
__safe_mem_acc.argtypes = [_ctypes.c_bool, _ctypes.c_size_t, __CALLBACK_TYPE]
__safe_mem_acc.restype = _ctypes.c_int

__write = __lib.write
__write.argtypes = [_ctypes.c_bool, _ctypes.c_void_p, _ctypes.POINTER(_ctypes.c_char), _ctypes.c_size_t]
__write.restype = _ctypes.c_int

__read = __lib.read
__read.argtypes = [_ctypes.c_bool, _ctypes.c_void_p, _ctypes.c_size_t]
__read.restype = _ctypes.POINTER(_ctypes.c_char)



__ERR_FAILED_ALLOC = 1
__ERR_NULL_PTR = 2



__DEBUG = False
def set_debug(debug_:"bool") -> "None":
	global __DEBUG
	__DEBUG = debug_



def memory_access(size_, callback_:"_Callable[[int],None]") -> "None":
	c_callback = __CALLBACK_TYPE(callback_)
	res = __safe_mem_acc(__DEBUG, size_, c_callback)
	if res != 0:
		if res == __ERR_FAILED_ALLOC:
			raise MemoryError("Failed to allocate memory.")
		else:
			raise Exception("Unknown error.")



def write(ptr_:"int", data_:"bytes"):
	res = __write(__DEBUG, ptr_, data_, len(data_))
	if res != 0:
		if res == __ERR_NULL_PTR:
			raise MemoryError("Memory pointer is null.")
		else:
			raise Exception("Unknown error.")



def read(ptr_:"int", size_:"int"):
	res = __read(__DEBUG, ptr_, size_)[:size_]
	if not res:
		raise MemoryError("Failed to read memory.")
	return res



if __name__ == "__main__":
	def callback(addr:int) -> None:
		print(f"Address: {addr}")
		
	memory_access(64, callback)
