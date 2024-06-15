import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from multiprocessing import Manager, Process
from refvars import new, Reference

def worker(shared_d:"dict[str,Reference]"):
	my_ref = shared_d["my_ref"]
	my_ref.set(my_ref.value + "!")

def main():
	ref = new[str]("Hello, World!").get_ref()

	manager = Manager()
	shared_dict = manager.dict()
	shared_dict["my_ref"] = ref

	p = Process(target=worker, args=(shared_dict,))
	p.start()
	p.join()

	assert ref.get() == "Hello, World!"

if __name__ == "__main__":
	main()
	print("Success!")
