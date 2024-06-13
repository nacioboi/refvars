# TODO for the `python_reference` repository

- [x] Add the option for runtime type checking.
- [ ] Add ability to read from starting point in `memlib.c`. This will speed up the process of reading the memory for large memory blocks.
- [ ] Think of more features or just ways to improve.

## Bug

We are checking stack frame to get the source code of the function.

This can lead to a bug if the line of code we are looking for is not 3rd index in the stack frame.

For eg, the bug happens when attaching a debugger to the code.

## Cool features

- [ ] Add a `List_Of_References` class that will add useful functions like:
  - `remove`,
  - `append`,
  - `insert`,
  - `pop`,

This will be useful over using standard lists for eg.

```python
from refvars import Reference, new



THREADS:"list[Reference]" = []



def _print_dot_and_wait(exit_flag:"Reference[bool]"):
	global THREADS
	# Look here, the below is needed because we want to remove the thread from the list when this function is done.
	# > It is also not entirely thread safe.
	ref = THREADS[-1]
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	# Since global `THREADS` is a list of References and not a list of threads, we cannot do the following:
	# `THREADS.remove(threading.current_thread())`: which is most convenient.
	THREADS.remove(ref)

def print_dots_and_wait():
	global THREADS
	t = threading.Thread(target=_print_dot_and_wait)
	ref = new[Any](t).get_ref()
	THREADS.append(ref)
	t.start()
```

The takeaway from the above code is that sometimes we need to remove/pop a reference from a list of references but using
the item contained in the reference instead of the reference itself.

The following proposed class will make this easier.

```python
from refvars import List_Of_References, new

THREADS:"List_Of_References" = List_Of_References()

def _print_dot_and_wait(exit_flag:"Reference[bool]"):
	global THREADS
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	if exit_flag.get() == False: return
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.5)
	THREADS.remove(threading.current_thread())

def print_dots_and_wait():
	global THREADS
	t = threading.Thread(target=_print_dot_and_wait)
	ref = new[Any](t).get_ref()
	THREADS.append(t)
	t.start()
```

Notice how the only change is in the type of `THREADS`.

- [ ] Add `Union` type support.
