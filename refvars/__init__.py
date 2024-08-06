from enum import IntEnum
from typing import Callable, Generic, TypeVar, Iterator, TypeVar
from numba import njit, experimental
from numba import types
import numpy as np
import inspect

from .lib_mem import allocate as _allocate, deallocate as _deallocate
from .lib_mem import write as _write, read as _read
from .il2bl import ilist_to_blist




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

@experimental.jitclass(spec={
	"address": types.int64,
	"size": types.int64,
	"base_type": types.int64,
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
		_deallocate(debug_, self.address)

	def write(self, data_:"bytes", debug_=False) -> "int":
		if len(data_) > self.size:
			return 1
		if debug_:
			print(f"Data: [{data_}]")
		x = [0]*len(data_)
		for i in range(len(data_)):
			x[i] = data_[i]
		if debug_:
			print(f"Generated numpy array...")
		b = ilist_to_blist(np.array(x, dtype=np.uint8))
		if debug_:
			print(f"Running `_write({debug_}, {self.address}, {b})`...")
		return _write(debug_, self.address, b)

	def spread(self, single_byte_:"bytes", debug_=False) -> "int":
		if len(single_byte_) != 1:
			return 1
		if debug_:
			print(f"Single byte: [{single_byte_}]")
		x = [0]*self.size
		for i in range(self.size):
			x[i] = single_byte_[0]
		if debug_:
			print(f"Generated numpy array...")
		b = ilist_to_blist(np.array(x, dtype=np.uint8))
		if debug_:
			print(f"Running `_write({debug_}, {self.address}, {b})`...")
		return _write(debug_, self.address, b)

	def read(self, debug_=False) -> "tuple[int,bytes]":
		if debug_:
			print(f"Running `_read({debug_}, {self.address}, {self.size})`...")
		res, bs = _read(debug_, self.address, self.size)
		if debug_:
			for b in bs:
				print(f"Byte: [{b}]")
			print(f"Res: [{res}]")
		data = ilist_to_blist(bs)
		if debug_:
			print(f"Data: [{data}]")
		return res, b"".join([b for b in data])

@experimental.jitclass(spec={
	"__base_size": types.int64,
})#type:ignore
class Allocation:
	def __init__(self, size_:"int"):
		self.__base_size = size_
	
	def unsafe_access(self, type_:"ALLOCATION_TYPE", debug_=False) -> "Pointer":
		ptr = _allocate(debug_, self.__base_size)
		return Pointer(
			ptr,
			self.__base_size,
			type_
		)

@njit(cache=False)
def alloc(size_:"int") -> "Allocation":
	return Allocation(size_)


