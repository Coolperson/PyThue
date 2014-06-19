"""
	PyThue - The python Thue interpreter
	by Daniel Swann

	Usage: thue.py <filename>

	Licensed under the WTFPL
	See LICENSE for details
"""

import random
import sys


CAN_BE = "::="
INPUT_STREAM = ":::"
OUTPUT_STREAM = "~"


class ThueError(Exception):
	def __init__(self, value):
		self.value = value


class ThueParser:
	def __init__(self):
		self.rules = []
		self.current = []
		self.statement = None

	def build(self, stream):
		lines = stream.split("\n")
		rules_complete = False
		for line in lines:
			if line.find(CAN_BE) > 0:
				self.rules.append(line.split(CAN_BE))
			elif line.find(CAN_BE) == 0:
				rules_complete = True
				continue
			if rules_complete and len(line) > 0:
				self.statement = line
				break
		if len(self.rules) == 0:
			raise ThueError("No rules detected!")
		if self.statement is None:
			raise ThueError("No statement detected!")
		self.current = list(self.rules)

	def step(self):
		index = random.randint(0, len(self.current) - 1)
		lhs = self.current[index][0]
		rhs = self.current[index][1]
		if lhs in self.statement:
			if rhs[0] == OUTPUT_STREAM:
				print(rhs[1:])
				self.statement = self.statement.replace(lhs, "", 1)
			elif rhs == INPUT_STREAM:
				query = input("%s=" % lhs)
				self.statement = self.statement.replace(lhs, query, 1)
			else:
				self.statement = self.statement.replace(lhs, rhs, 1)
			self.current = list(self.rules)
		else:
			self.current.pop(index)

	def execute(self):
		while len(self.current) > 0:
			self.step()


if __name__ == "__main__":
	if len(sys.argv) == 2:
		t = ThueParser()
		with open(sys.argv[1]) as f:
			t.build(f.read())
		t.execute()
		print(t.statement)
	else:
		print("thue.py <filename>")
		sys.exit(1)