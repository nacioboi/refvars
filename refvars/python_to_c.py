from typing import Callable
from refvars import Reference

from numba import njit as _njit
import ctypes as _ctypes



_REQUEST_CALLBACK = _ctypes.CFUNCTYPE(_ctypes.c_char_p, _ctypes.c_int)
_RESULT_CALLBACK = _ctypes.CFUNCTYPE(_ctypes.c_bool, _ctypes.c_char_p)



@_njit(cache=True, fastmath=True)
def decoder(ptr):
	s = []
	for i in range(len(ptr)):
		s.append(chr(ptr[i]))
	return "".join(s)



class Python_To_C:
	def __init__(self, njit_request_giver, njit_result_receiver):
		self.request_callback_ctypes = _REQUEST_CALLBACK(njit_request_giver)
		self.result_callback_ctypes = _RESULT_CALLBACK(njit_result_receiver)

	def start_service(self, dll_path):
		dll = _ctypes.CDLL(dll_path)
		dll.service.argtypes = [_REQUEST_CALLBACK, _RESULT_CALLBACK]
		dll.service.restype = None
		dll.service(
			self.request_callback_ctypes,
			self.result_callback_ctypes
		)


