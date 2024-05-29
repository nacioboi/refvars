from dataclasses import dataclass
import datetime
import os



class Normal_People_Date:

	def __new__(cls, day_:"int", month_:"int", year_:"int") -> "datetime.date":
		return datetime.date(year_, month_, day_)
	


@dataclass
class Version:

	date: datetime.date
	version_number: str
	notes: str|None

	def validate(self):
		s = self.version_number.split(".")
		if not len(s) == 2:
			raise ValueError("Version number must have exactly 2 parts.")
		for i in s:
			if not i.isdigit():
				raise ValueError("Version number must be numeric.")

	def repr_date(self) -> str:
		day_p = str(self.date.day)
		if day_p.endswith("1"):
			day_p = "st"
		elif day_p.endswith("2"):
			day_p = "nd"
		elif day_p.endswith("3"):
			day_p = "rd"
		else:
			day_p = "th"
		return f"{self.date.day}{day_p}/{self.date.month}/{self.date.year}"



def init_description() -> str:
	description = None
	with open("README.md", "r") as f:
		description = f.read()
	if description is None:
		raise Exception("README.md is empty.")
	return description



def clear_screen():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")



def get_y_n(question:str) -> bool:
	while True:
		answer = input(question)
		if answer.lower() == "y":
			return True
		elif answer.lower() == "n":
			return False
		else:
			print("Please enter 'y' or 'n'.")

