from typing import Any, Callable
from refvars import Reference

from numba import njit as _njit
import ctypes as _ctypes
import numpy as _np



_REQUEST_CALLBACK = _ctypes.CFUNCTYPE(_ctypes.c_bool, _ctypes.c_int, _ctypes.c_void_p, _ctypes.c_int)
_RESULT_CALLBACK = _ctypes.CFUNCTYPE(_ctypes.c_bool, _ctypes.c_char_p)



@_njit(cache=True, fastmath=True)
def _decoder(ptr):
	s = []
	for i in range(len(ptr)):
		s.append(chr(ptr[i]))
	return "".join(s)



class Python_To_C:
	def __init__(self,
			njit_request_giver:"Callable[[int,int],tuple[list[int],bool]]",
			njit_result_receiver:"Callable[[str],bool]"
	) -> "None":
		self.__request_giver = njit_request_giver
		self.__result_receiver = njit_result_receiver
		self.__buff = None
		self.__exit_flag = False
		self.request_callback_ctypes = _REQUEST_CALLBACK(self.__request_giver_wrapper)
		self.result_callback_ctypes = _RESULT_CALLBACK(self.__result_receiver_wrapper)


	def __request_giver_wrapper(self, index, ptr, size) -> "bool":
		data, keep_going = self.__request_giver(index, size)
		if not self.__buff:
			self.__buff = _np.frombuffer((_ctypes.c_char*size).from_address(ptr), dtype=_np.uint8)
		self.__buff[:len(data)] = data
		return keep_going
	
	def __result_receiver_wrapper(self, ptr):
		return self.__result_receiver(_decoder(ptr))
	
	def bootstrap_service(self, dll_path):
		dll = _ctypes.CDLL(f"./{dll_path}")
		dll.service.argtypes = [_REQUEST_CALLBACK, _RESULT_CALLBACK, _ctypes.c_int32, _ctypes.c_int64]
		dll.service.restype = None
		self.dll = dll
	
	def start_service(self, buff_size, sleep_interval=25):
		self.dll.service(
			self.request_callback_ctypes,
			self.result_callback_ctypes,
			buff_size,
			sleep_interval
		)


