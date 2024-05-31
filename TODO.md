# TODO for the `python_reference` repository

- [x] Add the option for runtime type checking.
- [ ] Add ability to read from starting point in `memlib.c`. This will speed up the process of reading the memory for large memory blocks.
- [ ] Think of more features or just ways to improve.

## Bug

We are checking stack frame to get the source code of the function.

This can lead to a bug if the line of code we are looking for is not 3rd index in the stack frame.

For eg, the bug happens when attaching a debugger to the code.
