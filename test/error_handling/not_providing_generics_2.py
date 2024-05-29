import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from refvars import new

# NOTE: The below should raise a TypeError.
my_ref1 = new[bool](0).get_ref() #type:ignore
#my_ref2=new[bool](0).get_ref() #type:ignore
#my_ref3 		=	new[bool](0).get_ref() #type:ignore
#my_ref4 =new[bool](0).get_ref() #type:ignore
#my_ref5 \
#	= new[bool](0).get_ref() #type:ignore

