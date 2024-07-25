import ctypes as _ctypes
from typing import Callable as _Callable
from os.path import abspath, exists, join, dirname
from platform import machine
from sys import platform

arch = machine().strip().upper()
platform = platform.strip().upper()
if arch == "AMD64" and platform == "WIN32":
	DLL_NAME = "lib_mem_win_x86.dll"
elif arch == "ARM64" and platform == "DARWIN":
	DLL_NAME = "lib_mem_mac_arm64.dylib"
else:
	err_msg = f"Unsupported platform=[{platform}], architecture=[{arch}] combination."
	raise Exception(err_msg)

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

__allocate = __lib.allocate
__allocate.argtypes = [_ctypes.c_bool, _ctypes.c_size_t]
__allocate.restype = _ctypes.c_void_p

__deallocate = __lib.deallocate
__deallocate.argtypes = [_ctypes.c_bool, _ctypes.c_void_p]
__deallocate.restype = _ctypes.c_int



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



def _allocate(size_:"int") -> "int":
	ptr = __allocate(__DEBUG, size_)
	if not ptr:
		raise MemoryError("Failed to allocate memory.")
	return ptr



def _deallocate(ptr_:"int") -> "int":
	res = __deallocate(__DEBUG, ptr_)
	if res != 0:
		print(MemoryError("Failed to deallocate memory."))
	return res


def write(ptr_:"int", data_:"bytes"):
	res = __write(__DEBUG, ptr_, data_, len(data_))
	if res != 0:
		if res == __ERR_NULL_PTR:
			raise MemoryError("Memory pointer is null.")
		else:
			raise Exception("Unknown error.")



def read(ptr_:"int", size_:"int"):
	res = __read(True, ptr_, size_)[:size_]
	if not res:
		raise MemoryError("Failed to read memory.")
	return res



__start_mmf_service = __lib.start_mmf_service
__start_mmf_service.argtypes = [_ctypes.c_bool, _ctypes.c_char_p, _ctypes.c_int, _ctypes.c_int]
__start_mmf_service.restype = _ctypes.c_int

__stop_mmf_service = __lib.stop_mmf_service
__stop_mmf_service.argtypes = [_ctypes.c_bool]
__stop_mmf_service.restype = _ctypes.c_int

__get_mmf_ptr = __lib.get_mmf_ptr
__get_mmf_ptr.argtypes = [_ctypes.c_bool]
__get_mmf_ptr.restype = _ctypes.c_void_p

__grow_mmf_service = __lib.grow_mmf_service
__grow_mmf_service.argtypes = [_ctypes.c_bool, _ctypes.POINTER(_ctypes.c_char), _ctypes.c_int, _ctypes.c_int]
__grow_mmf_service.restype = _ctypes.c_int

__shrink_mmf_service = __lib.shrink_mmf_service
__shrink_mmf_service.argtypes = [_ctypes.c_bool, _ctypes.POINTER(_ctypes.c_char), _ctypes.c_int, _ctypes.c_int]
__shrink_mmf_service.restype = _ctypes.c_int

def start_mmf_service(name, size_low, size_high):
	return __start_mmf_service(__DEBUG, name, size_low, size_high)

def stop_mmf_service():
	return __stop_mmf_service(__DEBUG)

def grow_mmf_service(name, size_low, size_high):
	return __grow_mmf_service(__DEBUG, name, size_low, size_high)

def shrink_mmf_service(name, size_low, size_high):
	return __shrink_mmf_service(__DEBUG, name, size_low, size_high)

def get_mmf_ptr() -> "int":
	res = __get_mmf_ptr(__DEBUG)
	if not res:
		raise MemoryError("Failed to get MMF pointer.")
	return res


