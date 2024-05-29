import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from refvars import new

new[bool](False).get_ref()

import refvars

refvars.new[bool](False).get_ref()

print("Success!")
