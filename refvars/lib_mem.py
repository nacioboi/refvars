import ctypes as _ctypes
from numba import njit as _njit
import numpy as np
from typing import Callable as _Callable
from platform import machine as _machine
from sys import platform as _platform
from os import path as _path

_ARCH = _machine().strip().upper()
_PLATFORM = _platform.strip().upper()
if _ARCH == "AMD64" and _PLATFORM == "WIN32":
	_DLL_NAME = "lib_mem_win_x86.dll"
elif _ARCH == "ARM64" and _PLATFORM == "DARWIN":
	_DLL_NAME = "lib_mem_mac_arm64.dylib"
else:
	err_msg = f"Unsupported platform=[{_PLATFORM}], architecture=[{_ARCH}] combination."
	raise Exception(err_msg)

_BASE_DIR = _path.dirname(__file__)
_DLL_PATH = _path.abspath(_path.join(_BASE_DIR, _DLL_NAME))

if not _path.exists(_DLL_PATH):
	raise FileNotFoundError(f"[{_DLL_PATH}] not found in the same directory as this script.")



__lib = _ctypes.CDLL(_DLL_PATH)

__CALLBACK_TYPE = _ctypes.CFUNCTYPE(None, _ctypes.c_void_p)

__safe_mem_acc = __lib.safe_memory_access
__safe_mem_acc.argtypes = [_ctypes.c_bool, _ctypes.c_size_t, __CALLBACK_TYPE]
__safe_mem_acc.restype = _ctypes.c_int

__write = __lib.write
__write.argtypes = [_ctypes.c_bool, _ctypes.c_void_p, _ctypes.c_void_p, _ctypes.c_size_t]
__write.restype = _ctypes.c_int

__read = __lib.read
__read.argtypes = [_ctypes.c_bool, _ctypes.c_void_p, _ctypes.c_size_t, _ctypes.c_void_p]
__read.restype = None

__allocate = __lib.allocate
__allocate.argtypes = [_ctypes.c_bool, _ctypes.c_size_t]
__allocate.restype = _ctypes.c_void_p

__deallocate = __lib.deallocate
__deallocate.argtypes = [_ctypes.c_bool, _ctypes.c_void_p]
__deallocate.restype = _ctypes.c_int



@_njit(cache=True)
def memory_access(debug_:"bool", size_:"int", callback_:"_Callable[[int],None]") -> "int":
	c_callback = __CALLBACK_TYPE(callback_)
	return __safe_mem_acc(debug_, size_, c_callback)

@_njit(cache=False)
def allocate(debug_:"bool", size_:"int") -> "int":
	return __allocate(debug_, size_)

@_njit(cache=False)
def deallocate(debug_:"bool", ptr_:"int") -> "int":
	return __deallocate(debug_, ptr_)

@_njit(cache=False)
def write(debug_:"bool", ptr_:"int", data_:"bytes") -> "int":
	data = np.frombuffer(data_, dtype=np.uint8)
	return __write(debug_, ptr_, data.ctypes.data, len(data))


@_njit(cache=False)
def read(debug_:"bool", ptr_:"int", size_:"int") -> "bytes":
	out = np.zeros(size_, dtype=np.uint8)
	__read(debug_, ptr_, size_, out.ctypes.data)
	return out



__start_mmf_service = __lib.start_mmf_service
__start_mmf_service.argtypes = [_ctypes.c_bool, _ctypes.c_void_p, _ctypes.c_int, _ctypes.c_int]
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



_LARGEST_32_BIT_INT = 2**32 - 1



def start_mmf_service(debug_:"bool", name_:"bytes", size_low_:"int", size_high_:"int") -> "int":
	if not (size_low_ < _LARGEST_32_BIT_INT > size_high_ and size_low_ > 0 <= size_high_):
		raise ValueError("Both size parameters must be a valid 32-bit unsigned int.")
	return __start_mmf_service(debug_, name_, size_low_, size_high_)

def stop_mmf_service(debug_:"bool") -> "int":
	return __stop_mmf_service(debug_)

def grow_mmf_service(debug_:"bool", name_:"str", lrgr_size_low_:"int", lrgr_size_high_:"int") -> "int":
	if not (lrgr_size_low_ < _LARGEST_32_BIT_INT > lrgr_size_high_ and lrgr_size_low_ > 0 <= lrgr_size_high_):
		raise ValueError("Both size parameters must be a valid 32-bit unsigned int.")
	return __grow_mmf_service(debug_, name_, lrgr_size_low_, lrgr_size_high_)

def shrink_mmf_service(debug_:"bool", name_:"str", smlr_size_low_:"int", smlr_size_high_:"int") -> "int":
	if not (smlr_size_low_ < _LARGEST_32_BIT_INT > smlr_size_high_ and smlr_size_low_ > 0 <= smlr_size_high_):
		raise ValueError("Both size parameters must be a valid 32-bit unsigned int.")
	return __shrink_mmf_service(debug_, name_, smlr_size_low_, smlr_size_high_)

def get_mmf_ptr(debug_:"bool") -> "int":
	return __get_mmf_ptr(debug_)


