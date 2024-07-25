# TODO for the `python_reference` repository

- [x] Add the option for runtime type checking.
- [ ] Add ability to read from starting point in `memlib.c`. This will speed up the process of reading the memory for large memory blocks.
- [ ] Think of more features or just ways to improve.

## Bug

We are checking stack frame to get the source code of the function.

This can lead to a bug if the line of code we are looking for is not 3rd index in the stack frame.

For eg, the bug happens when attaching a debugger to the code.

## Cool features

- [x] Add a `List_Of_References` class that will add useful functions like:
  - `remove`,
  - `append`,
  - `insert`,
  - `pop`,
- [x] Add `Union` type support.
- [ ] Add Basic IPC support using memory mapped files.
  - [x] On windows.
  - [ ] On linux.
  - [ ] On mac.

## IPC via MMF TODO

- [ ] Test thread safety in Windows.
  - We layed the groundwork for this using the critical section feature in Windows.
- [ ] Test MMF on Linux.
- [ ] Test thread safety in Linux.
- [ ] Before committing too hard to one API, we should test the usage of the API to see if it is easy to use.

The performance gains we can achieve with MMF are huge, provided that we also use numba/numpy along with multiprocessing.

- [ ] Test compilation via numba.

