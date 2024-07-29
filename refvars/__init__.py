from typing import Any, Callable, Generic, Iterator, TypeVar
import inspect



_T_PYTHON_REFERENCE = TypeVar('_T_PYTHON_REFERENCE')
_REF_VARS_SPECIAL_SAUCE = False
_DO_RUNTIME_USAGE_CHECKS = True
def disable_runtime_usage_checks():
	global _DO_RUNTIME_USAGE_CHECKS
	_DO_RUNTIME_USAGE_CHECKS = False



class Reference (Generic[_T_PYTHON_REFERENCE]):
	def __init__(self, type_:"str", value_:"_T_PYTHON_REFERENCE", do_runtime_usage_checks_:"bool"):
		global _REF_VARS_SPECIAL_SAUCE
		if _REF_VARS_SPECIAL_SAUCE == True:
			self.type = type_
			self.value = value_
			self.__do_runtime_usage_checks = do_runtime_usage_checks_
		else:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Do not instantiate the class `Reference` directly.\n"
			err_msg += f"Instead, use the class `new`.\n"
			raise SyntaxError(err_msg)

	def get(self) -> "_T_PYTHON_REFERENCE":
		return self.value

	def set(self, value_:"_T_PYTHON_REFERENCE"):
		possible_types = []
		if self.type.startswith("Union["):
			possible_types = self.type.split("[", 1)[1].split("]")[0].split(",")
			possible_types = [x.strip() for x in possible_types]
		else:
			possible_types = [self.type]
		if self.__do_runtime_usage_checks and value_.__class__.__name__ not in possible_types:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Argument 1 of `Reference.set` is not of type [{self.type}].\n"
			raise TypeError(err_msg)
		self.value = value_



class new (Generic[_T_PYTHON_REFERENCE]):
	def __init__(self, value_:"_T_PYTHON_REFERENCE"):
		global _REF_VARS_SPECIAL_SAUCE
		global _DO_RUNTIME_USAGE_CHECKS
		self.__type = value_.__class__.__name__
		if _DO_RUNTIME_USAGE_CHECKS:
			maybe_union_type = self._validate()
			if maybe_union_type.startswith("Union["):
				self.__type = maybe_union_type
		try:
			_REF_VARS_SPECIAL_SAUCE = True
			self.__reference = Reference[type(value_)](self.__type, value_, _DO_RUNTIME_USAGE_CHECKS)
		finally:
			_REF_VARS_SPECIAL_SAUCE = False

	def get_ref(self) -> "Reference[_T_PYTHON_REFERENCE]":
		return self.__reference

	def __validate_type(self, line_:"str") -> "str":
		# Need to get the type of the class.
		# The type is the part of the line after the square brackets.
		s = line_
		error_to_raise = 0
		try:
			s = s.split("[", 1)[1].strip()
			s = "".join(s.split("]")[0:-1]).strip()
		except IndexError:
			error_to_raise = 1
		if error_to_raise == 1:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"For the class `new`, you MUST provide generic type in square brackets.\n"
			err_msg += f"Example of incorrect:  `my_ref = new(\"x\").get_ref()`.\n"
			err_msg += f"Example of correct:    `my_ref = new[bool](True).get_ref()`.\n"
			err_msg += f"                                    ~~~~~~ This is what you need.\n"
			raise SyntaxError(err_msg)
		if not s.startswith("Union["):
			if self.__type != s:
				err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
				err_msg += f"For the class `new`, the value passed in must match the generic.\n"
				err_msg += f"Example of incorrect:  `my_ref = new[bool](\"x\").get_ref()`.\n"
				err_msg += f"Example of correct:    `my_ref = new[bool](True).get_ref()`.\n"
				err_msg += f"> Notice the `True` is a correct value for the generic `bool`.\n"
				err_msg += f"> You tried to match the value type of [{self.__type}]"
				err_msg += f" with the generic type of [{s}].\n"
				raise SyntaxError(err_msg)
		else:
			s = s+"]"
		return s

	def _validate(self) -> "str":
		# Need to get the line where the class was instantiated.
		stack = inspect.stack()
		error_to_raise = 0
		line = None
		try:
			caller = None
			for stack_frame in stack:
				f_name = stack_frame.filename
				with open(f_name, "r") as f:
					ctx = f.readlines()
				l = ctx[stack_frame.lineno-1]
				l = l.strip().split("#")[0]
				if "=" in l:
					splitted = l.split("=")
					if len(splitted) > 1 and splitted[1].strip().startswith("new"):
						caller = stack_frame
						break
				else:
					if l.startswith("new") or l.startswith("refvars.new"):
						caller = stack_frame
						break
			if caller is None:
				error_to_raise = 3
			else:
				line_no = caller.lineno
				file = caller.filename
				with open(file, "r") as f:
					lines = f.readlines()
				_line = lines[line_no-1]
				line = _line.strip().split("#")[0]
				if not line.strip().endswith(".get_ref()"):
					error_to_raise = 1
		except IndexError:
			error_to_raise = 2
		if error_to_raise == 1:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"For the class `new`, the class instantiation must be assigned using the syntax:\n"
			err_msg += f"  `my_ref = new[< type >](< initial value >).get_ref()`.\n"
			err_msg += f"                                            ~~~~~~~~~~\n"
			err_msg += f"The highlighted part is one in which you must add to the end of the instantiation.\n"
			err_msg += f"It must be exactly as printed and must be on the same line as the instantiation.\n"
			raise SyntaxError(err_msg)
		assert line is not None
		return self.__validate_type(line)



class List_Of_References (Generic[_T_PYTHON_REFERENCE]):
	def __init__(self) -> None:
		super().__init__()
		self.__internal_list:"list[Reference[_T_PYTHON_REFERENCE]]" = []
	
	def get(self) -> "list[Reference[_T_PYTHON_REFERENCE]]":
		return self.__internal_list

	def append(self, ref:"Reference[_T_PYTHON_REFERENCE]") -> None:
		self.__internal_list.append(ref)
	
	def extend(self, refs:"list[Reference[_T_PYTHON_REFERENCE]]") -> None:
		self.__internal_list.extend(refs)
	
	def append_item(self, item:"_T_PYTHON_REFERENCE") -> None:
		global _DO_RUNTIME_USAGE_CHECKS
		try:
			_DO_RUNTIME_USAGE_CHECKS = False
			new_ref = new[_T_PYTHON_REFERENCE](item).get_ref()
			self.__internal_list.append(new_ref)
		finally:
			_DO_RUNTIME_USAGE_CHECKS = True
	
	
	def extend_items(self, items:"list[_T_PYTHON_REFERENCE]") -> None:
		global _DO_RUNTIME_USAGE_CHECKS
		for item in items:
			try:
				_DO_RUNTIME_USAGE_CHECKS = False
				new_ref = new[_T_PYTHON_REFERENCE](item).get_ref()
				self.__internal_list.append(new_ref)
			finally:
				_DO_RUNTIME_USAGE_CHECKS = True

	def remove(self, ref:"Reference[_T_PYTHON_REFERENCE]") -> None:
		self.__internal_list.remove(ref)

	def remove_item(self, item:"_T_PYTHON_REFERENCE") -> None:
		for ref in self.__internal_list:
			if ref.get() == item:
				self.__internal_list.remove(ref)
				break
	
	def remove_all_items(self, item:"_T_PYTHON_REFERENCE") -> None:
		for ref in self.__internal_list:
			if ref.get() == item:
				self.__internal_list.remove(ref)
	
	def clear(self) -> None:
		self.__internal_list.clear()

	def __len__(self) -> "int":
		return len(self.__internal_list)
	
	def __getitem__(self, index:"int") -> "Reference[_T_PYTHON_REFERENCE]":
		return self.__internal_list[index]
	
	def __setitem__(self, index:"int", value:"Reference[_T_PYTHON_REFERENCE]") -> None:
		self.__internal_list[index] = value

	def __delitem__(self, index:"int") -> None:
		del self.__internal_list[index]

	def __iter__(self) -> "Iterator[Reference[_T_PYTHON_REFERENCE]]":
		return iter(self.__internal_list)
	
	def __reversed__(self) -> "Iterator[Reference[_T_PYTHON_REFERENCE]]":
		return reversed(self.__internal_list)
	
	def __contains__(self, item:"_T_PYTHON_REFERENCE") -> "bool":
		for ref in self.__internal_list:
			if ref.get() == item:
				return True
		return False
	
	def index(self, item:"_T_PYTHON_REFERENCE") -> "int":
		for i, ref in enumerate(self.__internal_list):
			if ref.get() == item:
				return i
		raise ValueError("Item not found.")
	
	def count(self, item:"_T_PYTHON_REFERENCE") -> "int":
		count = 0
		for ref in self.__internal_list:
			if ref.get() == item:
				count += 1
		return count
	
	def sort(self,
			key:"Callable[[Reference[_T_PYTHON_REFERENCE]],_T_PYTHON_REFERENCE]|None"=None,
			reverse:"bool"=False
	) -> None:
		assert len(self.__internal_list) > 0
		assert hasattr(self.__internal_list[0].value, "__lt__")
		if key is None:
			self.__internal_list.sort(key=lambda x: x.value, reverse=reverse) #type:ignore
			return
		self.__internal_list.sort(key=key, reverse=reverse) #type:ignore

	def reverse(self) -> None:
		self.__internal_list.reverse()

	def copy(self) -> "List_Of_References[_T_PYTHON_REFERENCE]":
		new_list = List_Of_References()
		new_list.extend(self.__internal_list)
		return new_list



from enum import Enum
class _ALLOC_TYPES (Enum):
	INT_8 = "INT_8"
	U_INT_8 = "U_INT_8"
	INT_16 = "INT_16"
	U_INT_16 = "U_INT_16"
	INT_32 = "INT_32"
	U_INT_32 = "U_INT_32"
	INT_64 = "INT_64"
	U_INT_64 = "U_INT_64"
	FLOAT_32 = "FLOAT_32"
	FLOAT_64 = "FLOAT_64"
	BOOL = "BOOL"
	CHAR = "CHAR"
	PTR = "PTR"



class _CUSTOM_LOCK:
	def __init__(self, ptr:"Pointer") -> None:
		self.ptr = ptr

	def acquire(self) -> None:
		while self.ptr.read_bool() == True:
			pass
		self.ptr.write_bool(True)

	def release(self) -> None:
		self.ptr.write_bool(False)

	def __enter__(self):
		self.acquire()
		return self

	def __exit__(self, __,___,____):
		self.release()



class Pointer:

	"""
	Contains the address, size, data size, and type of the memory block.
	Allows for reading and writing to the memory block.
	Also checks for invalid arguments like type mismatch.
	"""

	def __init__(self,
			addr_:"int", size_:"int",
			# Private:
			_typed_:"list[_ALLOC_TYPES]|None"=None, _unsafe_free_cb_:"Callable[[],int]|None"=None
	) -> None:
		global _REF_VARS_SPECIAL_SAUCE
		if not _REF_VARS_SPECIAL_SAUCE == True:
			self._lock:"None|_CUSTOM_LOCK" = None
			self.address = addr_
			self.size = size_
			self.dsize = None if not _typed_ else self._get_data_size(_typed_)
			self._validate(size_, _typed_)
			self.__typed = None if not _typed_ else _typed_
			if self.__typed:
				self.spread(int(0).to_bytes(self.size, "little"))
			self._unsafe_free_cb_ = _unsafe_free_cb_
		else:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Do not instantiate the class `Pointer` directly.\n"
			err_msg += f"Instead, use the class `alloc`.\n"
			raise SyntaxError(err_msg)
	
	def _get_data_size(self, types_:"list[_ALLOC_TYPES]") -> "int":
		if types_ in [[_ALLOC_TYPES.INT_8,], [_ALLOC_TYPES.U_INT_8,]]:
			return 1 	# 1 byte
		if types_ in [[_ALLOC_TYPES.INT_16,], [_ALLOC_TYPES.U_INT_16,]]:
			return 2	# 2 bytes
		if types_ in [[_ALLOC_TYPES.INT_32,], [_ALLOC_TYPES.U_INT_32,], [_ALLOC_TYPES.FLOAT_32,]]:
			return 4
		if types_ in [[_ALLOC_TYPES.INT_64,], [_ALLOC_TYPES.U_INT_64,], [_ALLOC_TYPES.FLOAT_64,]]:
			return 8
		if types_ in [[_ALLOC_TYPES.BOOL,]]:
			return 1
		if types_ in [[_ALLOC_TYPES.CHAR,]]:
			return 1
		if types_ in [
				[_ALLOC_TYPES.INT_8, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.U_INT_8, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.BOOL, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.CHAR, _ALLOC_TYPES.PTR,],
			]:
			return 1
		if types_ in [
				[_ALLOC_TYPES.INT_16, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.U_INT_16, _ALLOC_TYPES.PTR,],
			]:
			return 2
		if types_ in [
				[_ALLOC_TYPES.INT_32, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.U_INT_32, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.FLOAT_32, _ALLOC_TYPES.PTR,],
			]:
			return 4
		if types_ in [
				[_ALLOC_TYPES.INT_64, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.U_INT_64, _ALLOC_TYPES.PTR,],
				[_ALLOC_TYPES.FLOAT_64, _ALLOC_TYPES.PTR,],
			]:
			return 8
		raise ValueError("Type not supported.")

	def _validate(self, size_:"int", types_:"list[_ALLOC_TYPES]|None") -> None:
		if types_ is None:
			return
		if types_[-1] == _ALLOC_TYPES.PTR:
			return
		assert len(types_) == 1
		assert size_ == 1, "Size*DSize mismatch."

	def spread(self, single_byte:"bytes") -> None:
		assert len(single_byte) == 1
		self.write(single_byte*self.size)

	def write(self, value_:"bytes") -> None:
		if self._lock:
			with self._lock:
				self.__write(value_)
		else:
			self.__write(value_)
	def __write(self, value_:"bytes") -> None:		
		from .lib_mem import write
		if len(value_) > self.size:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Out of bounds.\n"
			raise MemoryError(err_msg)
		write(self.address, value_)
	
	def read(self, size_:"int") -> "bytes":
		from .lib_mem import read
		if size_ > self.size:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Out of bounds.\n"
			raise MemoryError(err_msg)
		return read(self.address, size_)

	def read_int8(self) -> "bytes":
		if self.__typed and self.__typed != [_ALLOC_TYPES.INT_8,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import read
		return read(self.address, self.size)
	
	def write_int8(self, value_:"int") -> None:
		if self.__typed and self.__typed != [_ALLOC_TYPES.INT_8,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import write
		write(self.address, value_.to_bytes(1, "little"))

	def read_uint8(self) -> "int":
		if self.__typed and self.__typed != [_ALLOC_TYPES.U_INT_8,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import read
		return int.from_bytes(read(self.address, self.size), "little")
	
	def write_uint8(self, value_:"int") -> None:
		if self.__typed and self.__typed != [_ALLOC_TYPES.U_INT_8,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import write
		write(self.address, value_.to_bytes(1, "little"))
	
	def write_bool(self, value_:"bool") -> None:
		if self.__typed and self.__typed != [_ALLOC_TYPES.BOOL,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import write
		write(self.address, int(0 if value_ is False else 1).to_bytes(1, "little"))

	def read_bool(self) -> "bool":
		if self.__typed and self.__typed != [_ALLOC_TYPES.BOOL,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		from .lib_mem import read
		return bool(int.from_bytes(read(self.address, self.size), "little"))

	def write_str(self, value_:"str") -> None:
		if self.__typed and self.__typed != [_ALLOC_TYPES.CHAR, _ALLOC_TYPES.PTR,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		assert len(value_) < self.size, "Input is too long."
		self.spread(b"\0")
		self.write(value_.encode("utf-8"))

	def clear_str(self) -> None:
		if self.__typed and self.__typed != [_ALLOC_TYPES.CHAR, _ALLOC_TYPES.PTR,]:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Type mismatch.\n"
			raise ValueError(err_msg)
		self.spread(b"\0")

	def __str__(self) -> str:
		if self.__typed and self.__typed == [_ALLOC_TYPES.BOOL,]:
			return f"{'1' if self.read_bool() == True else '0'}"
		if self.__typed and self.__typed == [_ALLOC_TYPES.INT_8,]:
			return f"{self.read_int8()}"
		if self.__typed and self.__typed == [_ALLOC_TYPES.U_INT_8,]:
			return f"{self.read_uint8()}"
		if self.__typed and self.__typed == [_ALLOC_TYPES.CHAR, _ALLOC_TYPES.PTR,]:
			return self.read_str().decode('utf-8')
		raise ValueError("Type not set.")

	def read_str(self) -> "bytes":
		all_data = self.read(self.size)
		null_byte_index = all_data.find(b"\0")
		if null_byte_index == -1:
			raise ValueError("No null byte found.")
		return all_data[:null_byte_index]

	def _enable_lock(self, lock_:"_CUSTOM_LOCK") -> "Pointer":
		self._lock = lock_
		return self



class alloc:

	"""
	Ask the kernel for a memory block of a certain size.
	We also provide a way to access MFF (Memory Mapped Files), this allows for shared memory between processes.
	"""

	def safe_access(self, callback_:"Callable[[Pointer],None]") -> "None":
		from .lib_mem import memory_access
		def wrapper(_addr_:int) -> None:
			nonlocal callback_
			ptr = Pointer(_addr_, self.__size)
			callback_(ptr)
		memory_access(self.__size, wrapper)

	def unsafe_access(self, *types_:"_ALLOC_TYPES") -> "Pointer":
		from .lib_mem import allocate
		from .lib_mem import start_mmf_service, stop_mmf_service, get_mmf_ptr
		if self.__mmf_name:
			start_mmf_service(self.__mmf_name, self.__size, 0)
			ptr = get_mmf_ptr()
		else:
			ptr = allocate(self.__size)
		return Pointer(
			ptr,
			self.__size,
			_typed_=[*types_],
			_unsafe_free_cb_=lambda: self._PRIVATE_unsafe_free(ptr)
		)

	def _PRIVATE_unsafe_free(self, ptr_:"int") -> "int":
		from .lib_mem import deallocate
		return deallocate(ptr_)

	def _validate(self):
		# Need to get the line where the class was instantiated.
		stack = inspect.stack()
		caller = stack[-1]
		line_no = caller.lineno
		file = caller.filename
		with open(file, "r") as f:
			lines = f.readlines()
		_line = lines[line_no-1]
		line = _line.strip().split("#")[0]
		#if not len(line.split(").safe_access(")) == 2:
		#	if len(line.split(").unsafe_access(")) == 2:
		#		return
		#	if len(line.split(".allocate(\"")) == 2:
		#		return
		#	err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
		#	err_msg += f"For the class `alloc`, the class instantiation must be assigned using the syntax:\n"
		#	err_msg += f"  `my_ptr = alloc(< size >).safe_access(< your callback >)`.\n"
		#	err_msg += f"                           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
		#	err_msg += f"The highlighted part is one in which you must add to the end of the instantiation.\n"
		#	err_msg += f"It must be exactly as printed and must be on the same line as the instantiation.\n"
		#	err_msg += f"\n"
		#	err_msg += f"Also note: The callback must be a function that takes `cb:'Callable[[int],None]'`.\n"
		#	err_msg += f"             The first argument is the memory address.\n"
		#	err_msg += f"             Do what ever you want with the memory address.\n"
		#	err_msg += f"             On return of the function, the memory will be freed.\n"
		#	err_msg += f"\n"
		#	err_msg += f"Final note: You may access your memory block UNSAFELY by using the following syntax:\n"
		#	err_msg += f"  `my_ptr = alloc(< size >).unsafe_access(< type : _S_ALLOC_TYPES:Enum >)`.\n"
		#	err_msg += f"                           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
		#	err_msg += f"Please use the `unsafe_access` method with caution.\n"
		#	raise SyntaxError(err_msg)
		
	def __init__(self, size_:"int", mmf_name_=None) -> None:
		global _REF_VARS_SPECIAL_SAUCE
		global _DO_RUNTIME_USAGE_CHECKS
		try:
			MAX_MALLOC_SIZE_IN_C = 18_446_744_073_709_551_615  # Unsigned 64-bit integer (unsigned long long).
			# We need to get the host architecture.
			if size_ < 0:
				err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
				err_msg += f"The size of the memory block must be a positive integer.\n"
				raise ValueError(err_msg)
			if size_ > MAX_MALLOC_SIZE_IN_C:
				err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
				err_msg += f"The size of the memory block is too large.\n"
				err_msg += f"Please use a size less than {MAX_MALLOC_SIZE_IN_C}.\n"
				raise ValueError(err_msg)
			self.__size = size_
			self.__mmf_name = mmf_name_
			self._validate()
		finally:
			_REF_VARS_SPECIAL_SAUCE = False



class Memory_Wrapper:
	def __init__(self, get_cb_) -> None:
		self.__get_cb = get_cb_
		self.t = _ALLOC_TYPES

		# Define some constants...
		self.TRUE = 1
		self.FALSE = 0
	
	def get(self, name_:"str") -> "Pointer":
		return self.__get_cb(name_)
	


class alloc_handler:

	"""
	A more structured way to handle memory allocation and deallocation.
	Features include:
	- Synchronized memory via an address book. Allows for shared memory between processes via MMF (Memory Mapped Files).
	- Hooks for handling memory changes.
	- Locking for write operations.
	"""

	def __LOCK(self, from_address=None) -> "_CUSTOM_LOCK":
		if from_address:
			return _CUSTOM_LOCK(from_address)
		ptr = alloc(1).unsafe_access(_ALLOC_TYPES.BOOL)
		ptr.write_bool(False)
		return _CUSTOM_LOCK(ptr)

	def __init__(self, address_book:"str|None"=None):
		self.__mapped:"dict[str,list[_ALLOC_TYPES]]" = {}
		self.__assigned:"dict[str,Pointer]" = {}
		self.__hooked:"dict[str,list[tuple[str,Callable[[alloc_handler,Memory_Wrapper],None]]]]" = {}
		self.__prev_state:"dict[str,bytes]" = {}
		self.__write_locks:"dict[str,_CUSTOM_LOCK]" = {}
		self.__is_master = False
		self.__enable_mmf = False
		from os import path
		self.__address_book = address_book
		if self.__address_book:
			self.__address_book = path.abspath(self.__address_book)
			if not path.exists(self.__address_book):
				with open(self.__address_book, "w") as f:
					self.__is_master = True
					self.__enable_mmf = True
					f.write("{}")
		if self.__address_book:
			self.__load_from_address_book()

	def __enter__(self):
		return self, Memory_Wrapper(self.__get)
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.shutdown()

	def __push_address(self, name_:"str", addr_:"int", size_:"int", types_:"list[_ALLOC_TYPES]") -> None:
		from json import load, dump
		from base64 import b64encode
		from pickle import dumps
		assert self.__address_book is not None
		with open(self.__address_book, "r") as f:
			data = load(f)
		attached_write_lock_addr = self.__write_locks[name_].ptr.address if self.__write_locks[name_] else None
		assert attached_write_lock_addr is not None
		data[name_] = (addr_, size_, b64encode(dumps(types_)).decode(), attached_write_lock_addr)
		with open(self.__address_book, "w") as f:
			dump(data, f)

	def __pop_address(self, name_:"str") -> "int":
		from json import load, dump
		assert self.__address_book is not None
		with open(self.__address_book, "r") as f:
			data = load(f)
		addr = data.pop(name_)
		with open(self.__address_book, "w") as f:
			dump(data, f)
		return addr

	def __load_from_address_book(self) -> "None":
		from json import load
		from base64 import b64decode
		from pickle import loads
		assert self.__address_book is not None
		with open(self.__address_book, "r") as f:
			data = load(f)
		def _PRIVATE_unsafe_free(ptr_:"int") -> "int":
			from .lib_mem import deallocate
			return deallocate(ptr_)
		for name, (addr, size, raw_types_data, lock_attached_ptr_addr) in data.items():
			types = loads(b64decode(raw_types_data))
			self.__mapped[name] = types
			self.__write_locks[name] = self.__LOCK(from_address=lock_attached_ptr_addr)
			ptr = Pointer(addr, size, types, lambda: _PRIVATE_unsafe_free(addr))
			ptr._lock = self.__write_locks[name]
			self.__assigned[name] = ptr

	def __allocate(self, name_, ptr_size_, *types_) -> "None":
			self.__mapped[name_] = [*types_,]
			self.__write_locks[name_] = self.__LOCK()
			mmf_name = None if not self.__enable_mmf else name_
			self.__assigned[name_] = alloc(ptr_size_, mmf_name_=mmf_name)\
				.unsafe_access(*types_)\
				._enable_lock(self.__write_locks[name_])
			if self.__address_book:
				x = self.__assigned[name_]
				self.__push_address(name_, x.address, x.size, [*types_,])
			self.__assigned[name_].spread(b"\0")

	def allocate(self, name_:"str", *types_:"_ALLOC_TYPES", eq_:"int|bytes|None"=None, ptr_size_:"int|None"=None) -> None:
		if name_ in self.__assigned:
			return
		if len(types_) == 1:
			type_ = types_[0]
			assert type_ == _ALLOC_TYPES.BOOL or type_ == _ALLOC_TYPES.INT_8 or type_ == _ALLOC_TYPES.U_INT_8
			ptr_size_ = 1
			self.__allocate(name_, ptr_size_, types_)
			if eq_ is not None:
				assert isinstance(eq_, int)
				self.__assigned[name_].write(eq_.to_bytes(1, "little"))
		else:
			e_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			e_msg += f"Only normal types along with [CHAR, PTR] are supported.\n"
			if len(types_) != 2:
				raise ValueError(e_msg)
			if [*types_,] != [_ALLOC_TYPES.CHAR, _ALLOC_TYPES.PTR]:
				raise ValueError(e_msg)
			if ptr_size_ is None:
				err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
				err_msg += f"Pointer size must be provided.\n"
				raise ValueError(err_msg)
			self.__allocate(name_, ptr_size_, types_)
			if eq_ is not None:
				assert isinstance(eq_, bytes)
				assert len(eq_) < ptr_size_, "Input is too long."
				self.__assigned[name_].spread(b"\0")
				self.__assigned[name_].write(eq_)
		
	def deallocate(self, name_:"str") -> "int":
		if name_ not in self.__assigned:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Variable not found.\n"
			raise ValueError(err_msg)
		
		cb = self.__assigned[name_]._unsafe_free_cb_
		assert cb is not None
		res = cb()
		del self.__assigned[name_]
		if self.__address_book:
			self.__pop_address(name_)
		return res

	def __get(self, name_:"str") -> "Pointer":
		t = self.__mapped.get(name_, None)
		if t is None:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Variable not found.\n"
			raise ValueError(err_msg)
		return self.__assigned[name_]
	
	def __handle_hooks(self) -> "None":
		while len(self.__hooked) > 0:
			for name, l in self.__hooked.items():
				for _, callback in l:
					prev_state = self.__prev_state.get(name, None)
					if prev_state is None:
						with self.__write_locks[name]:
							size = self.__assigned[name].size
							self.__prev_state[name] = self.__assigned[name].read(size)
					if prev_state != self.__assigned[name].read_bool():
						with self.__write_locks[name]:
							size = self.__assigned[name].size
							self.__prev_state[name] = self.__assigned[name].read(size)
							callback(self, Memory_Wrapper(self.__get))

	def out_hook(self, hook_candidate_:"str", id_:"str", callback_:"Callable[[alloc_handler,Memory_Wrapper],None]") -> "None":
		from threading import Thread
		if hook_candidate_ not in self.__hooked:
			self.__hooked[hook_candidate_] = []
		self.__hooked[hook_candidate_].append((id_, callback_))
		if len(self.__hooked) == 1:
			t = Thread(target=self.__handle_hooks, daemon=True)
			t.start()

	def unhook(self, hook_candidate_:"str", id_:"str") -> "None":
		if hook_candidate_ not in self.__hooked:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Hook not found.\n"
			raise ValueError(err_msg)
		for i, (id_, _) in enumerate(self.__hooked[hook_candidate_]):
			if id_ == id_:
				del self.__hooked[hook_candidate_][i]
		if len(self.__hooked) == 0:
			self.__prev_state.clear()
			self.__write_locks.clear()

	def shutdown(self, verbose=False) -> "None":
		if self.__is_master:
			while len(self.__assigned) > 0:
				name = list(self.__assigned.keys())[0]
				if verbose:
					print(f"Deallocating: [{name}]...")
				self.deallocate(name)
			if self.__address_book:
				from os import remove
				remove(self.__address_book)
		self.__hooked.clear()
		self.__prev_state.clear()
		self.__write_locks.clear()
		self.__assigned.clear()
		self.__mapped.clear()
	