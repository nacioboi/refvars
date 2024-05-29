import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import new

# NOTE: The below should raise a TypeError.
#my_ref1 = new(0).get_ref()
#my_ref2=new(0).get_ref()
#my_ref3 		=	new(0).get_ref()
#my_ref4 =new(0).get_ref()
#my_ref5 \
#	= new(0).get_ref()
my_ref6 = new(0).get_ref()  # Comments can be here.

