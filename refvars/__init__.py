from enum import IntEnum
from typing import Any, Callable
from numba import njit, experimental
from numba import int64
import numpy as np
import ctypes

from .lib_mem import allocate, deallocate, write as _write, read as _read


class ALLOCATION_TYPE (IntEnum):
	BOOL = 1
	UINT8 = 2
	INT8 = 3
	UINT16 = 4
	INT16 = 5
	UINT32 = 6
	INT32 = 7
	UINT64 = 8
	INT64 = 9

@njit(cache=True, fastmath=True)
def int_to_bytes_wtf(i:"int") -> "bytes":
	ret = []
	if i == 0:
		ret.append(b"\x00")
	elif i == 1:
		ret.append(b"\x01")
	elif i == 2:
		ret.append(b"\x02")
	elif i == 3:
		ret.append(b"\x03")
	elif i == 4:
		ret.append(b"\x04")
	elif i == 5:
		ret.append(b"\x05")
	elif i == 6:
		ret.append(b"\x06")
	elif i == 7:
		ret.append(b"\x07")
	elif i == 8:
		ret.append(b"\x08")
	elif i == 9:
		ret.append(b"\x09")
	elif i == 10:
		ret.append(b"\x0a")
	elif i == 11:
		ret.append(b"\x0b")
	elif i == 12:
		ret.append(b"\x0c")
	elif i == 13:
		ret.append(b"\x0d")
	elif i == 14:
		ret.append(b"\x0e")
	elif i == 15:
		ret.append(b"\x0f")
	elif i == 16:
		ret.append(b"\x10")
	elif i == 17:
		ret.append(b"\x11")
	elif i == 18:
		ret.append(b"\x12")
	elif i == 19:
		ret.append(b"\x13")
	elif i == 20:
		ret.append(b"\x14")
	elif i == 21:
		ret.append(b"\x15")
	elif i == 22:
		ret.append(b"\x16")
	elif i == 23:
		ret.append(b"\x17")
	elif i == 24:
		ret.append(b"\x18")
	elif i == 25:
		ret.append(b"\x19")
	elif i == 26:
		ret.append(b"\x1a")
	elif i == 27:
		ret.append(b"\x1b")
	elif i == 28:
		ret.append(b"\x1c")
	elif i == 29:
		ret.append(b"\x1d")
	elif i == 30:
		ret.append(b"\x1e")
	elif i == 31:
		ret.append(b"\x1f")
	elif i == 32:
		ret.append(b"\x20")
	elif i == 33:
		ret.append(b"\x21")
	elif i == 34:
		ret.append(b"\x22")
	elif i == 35:
		ret.append(b"\x23")
	elif i == 36:
		ret.append(b"\x24")
	elif i == 37:
		ret.append(b"\x25")
	elif i == 38:
		ret.append(b"\x26")
	elif i == 39:
		ret.append(b"\x27")
	elif i == 40:
		ret.append(b"\x28")
	elif i == 41:
		ret.append(b"\x29")
	elif i == 42:
		ret.append(b"\x2a")
	elif i == 43:
		ret.append(b"\x2b")
	elif i == 44:
		ret.append(b"\x2c")
	elif i == 45:
		ret.append(b"\x2d")
	elif i == 46:
		ret.append(b"\x2e")
	elif i == 47:
		ret.append(b"\x2f")
	elif i == 48:
		ret.append(b"\x30")
	elif i == 49:
		ret.append(b"\x31")
	elif i == 50:
		ret.append(b"\x32")
	elif i == 51:
		ret.append(b"\x33")
	elif i == 52:
		ret.append(b"\x34")
	elif i == 53:
		ret.append(b"\x35")
	elif i == 54:
		ret.append(b"\x36")
	elif i == 55:
		ret.append(b"\x37")
	elif i == 56:
		ret.append(b"\x38")
	elif i == 57:
		ret.append(b"\x39")
	elif i == 58:
		ret.append(b"\x3a")
	elif i == 59:
		ret.append(b"\x3b")
	elif i == 60:
		ret.append(b"\x3c")
	elif i == 61:
		ret.append(b"\x3d")
	elif i == 62:
		ret.append(b"\x3e")
	elif i == 63:
		ret.append(b"\x3f")
	elif i == 64:
		ret.append(b"\x40")
	elif i == 65:
		ret.append(b"\x41")
	elif i == 66:
		ret.append(b"\x42")
	elif i == 67:
		ret.append(b"\x43")
	elif i == 68:
		ret.append(b"\x44")
	elif i == 69:
		ret.append(b"\x45")
	elif i == 70:
		ret.append(b"\x46")
	elif i == 71:
		ret.append(b"\x47")
	elif i == 72:
		ret.append(b"\x48")
	elif i == 73:
		ret.append(b"\x49")
	elif i == 74:
		ret.append(b"\x4a")
	elif i == 75:
		ret.append(b"\x4b")
	elif i == 76:
		ret.append(b"\x4c")
	elif i == 77:
		ret.append(b"\x4d")
	elif i == 78:
		ret.append(b"\x4e")
	elif i == 79:
		ret.append(b"\x4f")
	elif i == 80:
		ret.append(b"\x50")
	elif i == 81:
		ret.append(b"\x51")
	elif i == 82:
		ret.append(b"\x52")
	elif i == 83:
		ret.append(b"\x53")
	elif i == 84:
		ret.append(b"\x54")
	elif i == 85:
		ret.append(b"\x55")
	elif i == 86:
		ret.append(b"\x56")
	elif i == 87:
		ret.append(b"\x57")
	elif i == 88:
		ret.append(b"\x58")
	elif i == 89:
		ret.append(b"\x59")
	elif i == 90:
		ret.append(b"\x5a")
	elif i == 91:
		ret.append(b"\x5b")
	elif i == 92:
		ret.append(b"\x5c")
	elif i == 93:
		ret.append(b"\x5d")
	elif i == 94:
		ret.append(b"\x5e")
	elif i == 95:
		ret.append(b"\x5f")
	elif i == 96:
		ret.append(b"\x60")
	elif i == 97:
		ret.append(b"\x61")
	elif i == 98:
		ret.append(b"\x62")
	elif i == 99:
		ret.append(b"\x63")
	elif i == 100:
		ret.append(b"\x64")
	elif i == 101:
		ret.append(b"\x65")
	elif i == 102:
		ret.append(b"\x66")
	elif i == 103:
		ret.append(b"\x67")
	elif i == 104:
		ret.append(b"\x68")
	elif i == 105:
		ret.append(b"\x69")
	elif i == 106:
		ret.append(b"\x6a")
	elif i == 107:
		ret.append(b"\x6b")
	elif i == 108:
		ret.append(b"\x6c")
	elif i == 109:
		ret.append(b"\x6d")
	elif i == 110:
		ret.append(b"\x6e")
	elif i == 111:
		ret.append(b"\x6f")
	elif i == 112:
		ret.append(b"\x70")
	elif i == 113:
		ret.append(b"\x71")
	elif i == 114:
		ret.append(b"\x72")
	elif i == 115:
		ret.append(b"\x73")
	elif i == 116:
		ret.append(b"\x74")
	elif i == 117:
		ret.append(b"\x75")
	elif i == 118:
		ret.append(b"\x76")
	elif i == 119:
		ret.append(b"\x77")
	elif i == 120:
		ret.append(b"\x78")
	elif i == 121:
		ret.append(b"\x79")
	elif i == 122:
		ret.append(b"\x7a")
	elif i == 123:
		ret.append(b"\x7b")
	elif i == 124:
		ret.append(b"\x7c")
	elif i == 125:
		ret.append(b"\x7d")
	elif i == 126:
		ret.append(b"\x7e")
	elif i == 127:
		ret.append(b"\x7f")
	elif i == 128:
		ret.append(b"\x80")
	elif i == 129:
		ret.append(b"\x81")
	elif i == 130:
		ret.append(b"\x82")
	elif i == 131:
		ret.append(b"\x83")
	elif i == 132:
		ret.append(b"\x84")
	elif i == 133:
		ret.append(b"\x85")
	elif i == 134:
		ret.append(b"\x86")
	elif i == 135:
		ret.append(b"\x87")
	elif i == 136:
		ret.append(b"\x88")
	elif i == 137:
		ret.append(b"\x89")
	elif i == 138:
		ret.append(b"\x8a")
	elif i == 139:
		ret.append(b"\x8b")
	elif i == 140:
		ret.append(b"\x8c")
	elif i == 141:
		ret.append(b"\x8d")
	elif i == 142:
		ret.append(b"\x8e")
	elif i == 143:
		ret.append(b"\x8f")
	elif i == 144:
		ret.append(b"\x90")
	elif i == 145:
		ret.append(b"\x91")
	elif i == 146:
		ret.append(b"\x92")
	elif i == 147:
		ret.append(b"\x93")
	elif i == 148:
		ret.append(b"\x94")
	elif i == 149:
		ret.append(b"\x95")
	elif i == 150:
		ret.append(b"\x96")
	elif i == 151:
		ret.append(b"\x97")
	elif i == 152:
		ret.append(b"\x98")
	elif i == 153:
		ret.append(b"\x99")
	elif i == 154:
		ret.append(b"\x9a")
	elif i == 155:
		ret.append(b"\x9b")
	elif i == 156:
		ret.append(b"\x9c")
	elif i == 157:
		ret.append(b"\x9d")
	elif i == 158:
		ret.append(b"\x9e")
	elif i == 159:
		ret.append(b"\x9f")
	elif i == 160:
		ret.append(b"\xa0")
	elif i == 161:
		ret.append(b"\xa1")
	elif i == 162:
		ret.append(b"\xa2")
	elif i == 163:
		ret.append(b"\xa3")
	elif i == 164:
		ret.append(b"\xa4")
	elif i == 165:
		ret.append(b"\xa5")
	elif i == 166:
		ret.append(b"\xa6")
	elif i == 167:
		ret.append(b"\xa7")
	elif i == 168:
		ret.append(b"\xa8")
	elif i == 169:
		ret.append(b"\xa9")
	elif i == 170:
		ret.append(b"\xaa")
	elif i == 171:
		ret.append(b"\xab")
	elif i == 172:
		ret.append(b"\xac")
	elif i == 173:
		ret.append(b"\xad")
	elif i == 174:
		ret.append(b"\xae")
	elif i == 175:
		ret.append(b"\xaf")
	elif i == 176:
		ret.append(b"\xb0")
	elif i == 177:
		ret.append(b"\xb1")
	elif i == 178:
		ret.append(b"\xb2")
	elif i == 179:
		ret.append(b"\xb3")
	elif i == 180:
		ret.append(b"\xb4")
	elif i == 181:
		ret.append(b"\xb5")
	elif i == 182:
		ret.append(b"\xb6")
	elif i == 183:
		ret.append(b"\xb7")
	elif i == 184:
		ret.append(b"\xb8")
	elif i == 185:
		ret.append(b"\xb9")
	elif i == 186:
		ret.append(b"\xba")
	elif i == 187:
		ret.append(b"\xbb")
	elif i == 188:
		ret.append(b"\xbc")
	elif i == 189:
		ret.append(b"\xbd")
	elif i == 190:
		ret.append(b"\xbe")
	elif i == 191:
		ret.append(b"\xbf")
	elif i == 192:
		ret.append(b"\xc0")
	elif i == 193:
		ret.append(b"\xc1")
	elif i == 194:
		ret.append(b"\xc2")
	elif i == 195:
		ret.append(b"\xc3")
	elif i == 196:
		ret.append(b"\xc4")
	elif i == 197:
		ret.append(b"\xc5")
	elif i == 198:
		ret.append(b"\xc6")
	elif i == 199:
		ret.append(b"\xc7")
	elif i == 200:
		ret.append(b"\xc8")
	elif i == 201:
		ret.append(b"\xc9")
	elif i == 202:
		ret.append(b"\xca")
	elif i == 203:
		ret.append(b"\xcb")
	elif i == 204:
		ret.append(b"\xcc")
	elif i == 205:
		ret.append(b"\xcd")
	elif i == 206:
		ret.append(b"\xce")
	elif i == 207:
		ret.append(b"\xcf")
	elif i == 208:
		ret.append(b"\xd0")
	elif i == 209:
		ret.append(b"\xd1")
	elif i == 210:
		ret.append(b"\xd2")
	elif i == 211:
		ret.append(b"\xd3")
	elif i == 212:
		ret.append(b"\xd4")
	elif i == 213:
		ret.append(b"\xd5")
	elif i == 214:
		ret.append(b"\xd6")
	elif i == 215:
		ret.append(b"\xd7")
	elif i == 216:
		ret.append(b"\xd8")
	elif i == 217:
		ret.append(b"\xd9")
	elif i == 218:
		ret.append(b"\xda")
	elif i == 219:
		ret.append(b"\xdb")
	elif i == 220:
		ret.append(b"\xdc")
	elif i == 221:
		ret.append(b"\xdd")
	elif i == 222:
		ret.append(b"\xde")
	elif i == 223:
		ret.append(b"\xdf")
	elif i == 224:
		ret.append(b"\xe0")
	elif i == 225:
		ret.append(b"\xe1")
	elif i == 226:
		ret.append(b"\xe2")
	elif i == 227:
		ret.append(b"\xe3")
	elif i == 228:
		ret.append(b"\xe4")
	elif i == 229:
		ret.append(b"\xe5")
	elif i == 230:
		ret.append(b"\xe6")
	elif i == 231:
		ret.append(b"\xe7")
	elif i == 232:
		ret.append(b"\xe8")
	elif i == 233:
		ret.append(b"\xe9")
	elif i == 234:
		ret.append(b"\xea")
	elif i == 235:
		ret.append(b"\xeb")
	elif i == 236:
		ret.append(b"\xec")
	elif i == 237:
		ret.append(b"\xed")
	elif i == 238:
		ret.append(b"\xee")
	elif i == 239:
		ret.append(b"\xef")
	elif i == 240:
		ret.append(b"\xf0")
	elif i == 241:
		ret.append(b"\xf1")
	elif i == 242:
		ret.append(b"\xf2")
	elif i == 243:
		ret.append(b"\xf3")
	elif i == 244:
		ret.append(b"\xf4")
	elif i == 245:
		ret.append(b"\xf5")
	elif i == 246:
		ret.append(b"\xf6")
	elif i == 247:
		ret.append(b"\xf7")
	elif i == 248:
		ret.append(b"\xf8")
	elif i == 249:
		ret.append(b"\xf9")
	elif i == 250:
		ret.append(b"\xfa")
	elif i == 251:
		ret.append(b"\xfb")
	elif i == 252:
		ret.append(b"\xfc")
	elif i == 253:
		ret.append(b"\xfd")
	elif i == 254:
		ret.append(b"\xfe")
	elif i == 255:
		ret.append(b"\xff")
	else:
		return b""
	return b"".join(ret)

@njit(cache=True, fastmath=True)
def ilist_to_blist_wtf(l:"np.ndarray",):
	return np.frombuffer(b"".join([
		b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09', b'\x0a', b'\x0b',
		b'\x0c', b'\x0d', b'\x0e', b'\x0f', b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17',
		b'\x18', b'\x19', b'\x1a', b'\x1b', b'\x1c', b'\x1d', b'\x1e', b'\x1f', b'\x20', b'\x21', b'\x22', b'\x23',
		b'\x24', b'\x25', b'\x26', b'\x27', b'\x28', b'\x29', b'\x2a', b'\x2b', b'\x2c', b'\x2d', b'\x2e', b'\x2f',
		b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3a', b'\x3b',
		b'\x3c', b'\x3d', b'\x3e', b'\x3f', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47',
		b'\x48', b'\x49', b'\x4a', b'\x4b', b'\x4c', b'\x4d', b'\x4e', b'\x4f', b'\x50', b'\x51', b'\x52', b'\x53',
		b'\x54', b'\x55', b'\x56', b'\x57', b'\x58', b'\x59', b'\x5a', b'\x5b', b'\x5c', b'\x5d', b'\x5e', b'\x5f',
		b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6a', b'\x6b',
		b'\x6c', b'\x6d', b'\x6e', b'\x6f', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77',
		b'\x78', b'\x79', b'\x7a', b'\x7b', b'\x7c', b'\x7d', b'\x7e', b'\x7f', b'\x80', b'\x81', b'\x82', b'\x83',
		b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f',
		b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98', b'\x99', b'\x9a', b'\x9b',
		b'\x9c', b'\x9d', b'\x9e', b'\x9f', b'\xa0', b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7',
		b'\xa8', b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf', b'\xb0', b'\xb1', b'\xb2', b'\xb3',
		b'\xb4', b'\xb5', b'\xb6', b'\xb7', b'\xb8', b'\xb9', b'\xba', b'\xbb', b'\xbc', b'\xbd', b'\xbe', b'\xbf',
		b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc4', b'\xc5', b'\xc6', b'\xc7', b'\xc8', b'\xc9', b'\xca', b'\xcb',
		b'\xcc', b'\xcd', b'\xce', b'\xcf', b'\xd0', b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6', b'\xd7',
		b'\xd8', b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf', b'\xe0', b'\xe1', b'\xe2', b'\xe3',
		b'\xe4', b'\xe5', b'\xe6', b'\xe7', b'\xe8', b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef',
		b'\xf0', b'\xf1', b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7', b'\xf8', b'\xf9', b'\xfa', b'\xfb',
		b'\xfc', b'\xfd', b'\xfe', b'\xff'
	]), dtype="S1")[l]

@experimental.jitclass(spec={
	"address": int64,
	"size": int64,
	"base_type": int64,
})#type:ignore
class Pointer:
	def __init__(self,
			address_:"int",
			size_:"int",
			base_type_:"ALLOCATION_TYPE",
	) -> None:
		self.address = address_
		self.size = size_
		self.base_type = base_type_
	
	def free(self, debug_=False) -> "None":
		deallocate(debug_, self.address)

	def write(self, data_:"str", debug_=False) -> "int":
		if len(data_) != self.size:
			return 1
		x = [0]*len(data_)
		for i in range(len(data_)):
			x[i] = ord(data_[i])
		b = ilist_to_blist_wtf(np.array(x, dtype=np.uint8))
		return _write(debug_, self.address, b)
	
	def read(self, debug_=False) -> "tuple[int,bytes]":
		res, bs = _read(debug_, self.address, self.size)
		data = ilist_to_blist_wtf(bs)
		return res, b"".join([b for b in data])

@experimental.jitclass(spec={
	"__base_size": int64,
})#type:ignore
class Allocation:
	def __init__(self, size_:"int"):
		self.__base_size = size_
	
	def unsafe_access(self, type_:"ALLOCATION_TYPE", debug_=False) -> "Pointer":
		ptr = allocate(debug_, self.__base_size)
		return Pointer(
			ptr,
			self.__base_size,
			type_
		)

@njit(cache=False)
def alloc(size_:"int") -> "Allocation":
	return Allocation(size_)


