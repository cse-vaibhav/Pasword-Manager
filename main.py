
from database import *

import clipboard as clip
import sys
import os
import logging

logging.disable()
logging.basicConfig(filename="logs.log",filemode="w", level=logging.DEBUG)

class PasswordManager:

	def __init__(self):
		self.db = Database()
		self.db.load()

		self.commands = {
			"help" : self.help,
			"save" : self.save,
			"get" : self.get,
			"delete" : self.delete,
			"import" : self.import_csv,
			"export" : self.export
		}

	def import_csv(self):
		return

	def export(self):
		return
	# prints the help message
	def help(self):
		print("""
	pm is a command-line utility to stores and ret11rieves all your passwords.

	Commands:

	help\t\t-\tshows this help page.
	get\t\t-\tcopies the password of the given webiste to the clipboard.
	save\t\t-\tstores the password of the given website.
	delete\t\t-\tdeletes an entry.
	export\t\t-\texport your data to a csv file
	import\t\t-\timport your data from a csv file

	Flags:

	--site\t\t-\tspecifies that argument given is a website.
	--username\t-\tspecifies that argument given is a username or email.
	--pwd\t\t-\tspecifiers that argument given is a password.

		""")

	# parses the email, password and username in the given arguments
	def parse_flags(self):
		# returns the index of arg in args and if not found returns -1
		def index(args, arg):
			try:
				return args.index(arg)
			except ValueError:
				return -1

		flgList = ["--site", "--username", "--pwd"]
		args = sys.argv[1:]
		self.flags = {x : "" for x in flgList}
		for flag in flgList:
			if index(args, flag) >= 0:
				self.flags[flag] = args[index(args, flag)+1]

	# deletes an entry
	def delete(self):
		args = list(self.flags.values())
		self.db.deleteEntry(args[1], args[0])
		print("Deleted Successfully")

	# copies the password to clipboard
	def get(self):
		args = list(self.flags.values())
		# if (len(args[0]) == 0 or len(args[1]) == 0):
		# 	raise MissingArgument()

		pwd = self.db.getEntry(args[1], args[0])
		if (len(pwd) == 0):
			raise NotFound()
		clip.copy(self.db.getEntry(args[1], args[0]))
		print("Password Copied to Clipboard")

	# save the details
	def save(self):
		args = list(self.flags.values())
		for x in args:
			if len(x) == 0:
				raise MissingArgument()

		self.db.addEntry(*args)
		print("Saved Successfully")

	def run(self):
		try:
			if (len(sys.argv) < 2):
				raise SyntaxError()

			# cmd = sys.argv[1]
			cmd = self.commands.get(sys.argv[1], None)
			if (cmd is None):
				raise SyntaxError()
			self.parse_flags()
			cmd()

		except Exception as e:
			e.err_msg()

		self.db.save()

if __name__ == "__main__":

	app = PasswordManager()
	app.run()
	# with open("pass.pkl", 'rb') as f:
	# 	tree1, tree2 = pickle.load(f)
	# print(tree1['x.com'].db)
	# print(tree2)

