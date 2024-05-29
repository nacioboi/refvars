import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import new

# Trying to trip our basic source checker.
my_ref1 = new[int](10).get_ref()
my_ref2=new[int](10).get_ref()
my_ref3 		=	new[int](10).get_ref()
my_ref4 =new[int](10).get_ref()
my_ref5 \
	= new[int](10).get_ref()
my_ref6 = new[int](10).get_ref()  # Comments can be here.

# TODO: THE BELOW IS NOT SUPPORTED YET.
#my_ref7 = new[int](10)\
#		.get_ref()

# TODO: THE BELOW IS NOT SUPPORTED YET.
#my_ref8 = new[int](10).get_ref() ; print(my_ref8.get())
