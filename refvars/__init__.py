from typing import Callable, Generic, TypeVar
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
		if self.__do_runtime_usage_checks and value_.__class__.__name__ != self.type:
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
			self._validate()
		try:
			_REF_VARS_SPECIAL_SAUCE = True
			self.__reference = Reference[type(value_)](self.__type, value_, _DO_RUNTIME_USAGE_CHECKS)
		finally:
			_REF_VARS_SPECIAL_SAUCE = False

	def get_ref(self) -> "Reference[_T_PYTHON_REFERENCE]":
		return self.__reference

	def __validate_type(self, line_:"str"):
		# Need to get the type of the class.
		# The type is the part of the line after the square brackets.
		s = line_
		error_to_raise = 0
		try:
			s = s.split("[")[1].strip()
			s = s.split("]")[0].strip()
		except IndexError:
			error_to_raise = 1
		if error_to_raise == 1:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"For the class `new`, you MUST provide generic type in square brackets.\n"
			err_msg += f"Example of incorrect:  `my_ref = new(\"x\").get_ref()`.\n"
			err_msg += f"Example of correct:    `my_ref = new[bool](True).get_ref()`.\n"
			err_msg += f"                                    ~~~~~~ This is what you need.\n"
			raise SyntaxError(err_msg)
		if self.__type != s:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"For the class `new`, the value passed in must match the generic.\n"
			err_msg += f"Example of incorrect:  `my_ref = new[bool](\"x\").get_ref()`.\n"
			err_msg += f"Example of correct:    `my_ref = new[bool](True).get_ref()`.\n"
			err_msg += f"> Notice the `True` is a correct value for the generic `bool`.\n"
			err_msg += f"> You tried to match the value type of [{self.__type}]"
			err_msg += f" with the generic type of [{s}].\n"
			raise SyntaxError(err_msg)

	def _validate(self):
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
		self.__validate_type(line)



class Pointer:
	def __init__(self, addr_:"int", size_:"int"):
		global _REF_VARS_SPECIAL_SAUCE
		if not _REF_VARS_SPECIAL_SAUCE == True:
			self.address = addr_
			self.size = size_
		else:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"Do not instantiate the class `Pointer` directly.\n"
			err_msg += f"Instead, use the class `alloc`.\n"
			raise SyntaxError(err_msg)
		
	def write(self, value_:"bytes") -> None:
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
	
	def read_until_null_byte(self) -> "bytes":
		all_data = self.read(self.size)
		null_byte_index = all_data.find(b"\0")
		if null_byte_index == -1:
			raise ValueError("No null byte found.")
		return all_data[:null_byte_index]



class alloc:
	def safe_access(self, callback_:"Callable[[Pointer],None]") -> "None":
		from .lib_mem import memory_access
		def wrapper(_addr_:int) -> None:
			nonlocal callback_
			ptr = Pointer(_addr_, self.__size)
			callback_(ptr)
		memory_access(self.__size, wrapper)

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
		if not len(line.split(").safe_access(")) == 2:
			err_msg = "\n\n[[[ ERROR FROM `refvars`! ]]]\n"
			err_msg += f"For the class `alloc`, the class instantiation must be assigned using the syntax:\n"
			err_msg += f"  `my_ptr = alloc(< size >).safe_access(< your callback >)`.\n"
			err_msg += f"                           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
			err_msg += f"The highlighted part is one in which you must add to the end of the instantiation.\n"
			err_msg += f"It must be exactly as printed and must be on the same line as the instantiation.\n"
			err_msg += f"\n"
			err_msg += f"Also note: The callback must be a function that takes `cb:'Callable[[int],None]'`.\n"
			err_msg += f"             The first argument is the memory address.\n"
			err_msg += f"             Do what ever you want with the memory address.\n"
			err_msg += f"             On return of the function, the memory will be freed.\n"
			raise SyntaxError(err_msg)
		
	def __init__(self, size_:"int") -> None:
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
			self._validate()
		finally:
			_REF_VARS_SPECIAL_SAUCE = False

