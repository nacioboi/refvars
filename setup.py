from _setup_deps import Version, Normal_People_Date, init_description, get_y_n, parse_notes, clear_screen

from setuptools import setup
import shutil
import sys
import os



NOTES = "\n"
NOTES += "Previous V0.2 didn't work.\n"
NOTES += " - Could not import the module.\n"
NOTES += " - The description did not appear on PyPi.\n"
NOTES += "This version hopefully fixes that."

CURRENT_VERSION = Version(
	date=Normal_People_Date(12, 4, 2024),
	version_number="0.6",
	notes=parse_notes(NOTES)
)
CURRENT_VERSION.validate()

LONG_DESCRIPTION = init_description()
LONG_DESCRIPTION += f"\n## V{CURRENT_VERSION.version_number} released on {CURRENT_VERSION.repr_date()}\n"
LONG_DESCRIPTION += NOTES



if not os.getcwd().endswith("refvars"):
	raise Exception("This script must be run from the root of the project directory.")



simple_path_checks = ["/examples/simple_example.py", "/examples/type_checking_example.py"]
if not all(os.path.exists(os.path.abspath(os.getcwd()+p)) for p in simple_path_checks):
	raise Exception("This script must be run from the root of the project directory.")



print("WARNING: ABOUT TO REMOVE THE `dist` DIRECTORY!!")
has_backed_up = get_y_n("Have you backed up the project? (y/n) ")
if not has_backed_up:
	exit(0)
shutil.rmtree("dist", ignore_errors=True)



if len(sys.argv) == 1:
	sys.argv.append("bdist_wheel")



setup(
	name="refvars",
	version=CURRENT_VERSION.version_number,
	keywords=[
		"python",
		"reference",
		"variables",
		"pointers",
		"output",
		"return",
		"types",
		"reference types",
		"refvars"
	],
	author="matrikater (Joel C. Watson)",
	author_email="matrikater@matriko.xyz",
	description="Solving one of Python's biggest problems. Reference types (output variables) are not implemented.",
	long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
	long_description=LONG_DESCRIPTION,
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
		"Natural Language :: English",
		"Topic :: Software Development :: Libraries :: Python Modules"
	],
)



print("\n] Setup complete.\n\n")
input("Press Enter to continue... ")
clear_screen()

print("Please review the following information before publishing:")
print(f"\tRelease Date: {CURRENT_VERSION.repr_date()}")
print(f"\tVersion Number: {CURRENT_VERSION.version_number}")
print(f"\tRelease Notes: \"{CURRENT_VERSION.notes}\"")
print(f"\tDescription is readable below...\n{LONG_DESCRIPTION}")

print()
did_check_version = get_y_n("Did you update the version information? (y/n) ")
if not did_check_version:
	exit(0)



do_publish = get_y_n("Would you like to publish to PyPi? (y/n) ")
if not do_publish:
	exit(0)

again_to_be_sure = get_y_n("ARE YOU SURE? Remember, you can't unpublish. (y/n) ")
if not again_to_be_sure:
	exit(0)

TOKEN = None
if os.path.exists(".token"):
	with open(".token", "r") as f:
		TOKEN = f.read().strip()
if TOKEN is None:
	def get_tok() -> str:
		t = input("Enter your PyPi token: ")
		if not get_y_n("Please confirm. Is it correct? (y/n) "):
			return get_tok()
		return t
	TOKEN = get_tok()
	with open(".token", "w") as f:
		f.write(TOKEN)

os.system(f"python3.11 -m twine upload --verbose --repository pypi -p \"{TOKEN}\" dist/*")
