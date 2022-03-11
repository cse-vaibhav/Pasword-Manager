
from database import *

import clipboard as clip
import sys
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

	help	-	shows this help page.
	get		-	copies the password of the given webiste to the clipboard.
	save	-	stores the password of the given website.
	delete	-	deletes an entry.
	export	-	export your data to a csv file
	import	-	import your data from a csv file

	Flags:

	--site	specifies that argument given is an email address.
	--username		-	specifies that argument given is a username or email.
	--pwd	-	specifiers that argument given is a password.

		""")

	# returns the index of arg in args and if not found returns -1
	def index(self, args, arg):
		try:
			return args.index(arg)
		except ValueError:
			return -1

	# parses the email, password and username in the given arguments
	def parse_flags(self):
		flgList = ["--site", "--username", "--pwd"]
		args = sys.argv[1:]
		self.flags = {x : "" for x in flgList}
		for flag in flgList:
			if self.index(args, flag) == -1:
				continue
			self.flags[flag] = args[self.index(args, flag)+1]

	# deletes an entry
	def delete(self):
		args = list(self.flags.values())
		self.db.deleteEntry(args[1], args[0])
		print("Deleted Successfully")
		return

	# copies the password according to arguments to clipboard
	def get(self):
		args = list(self.flags.values())
		# if (len(args[0]) == 0 or len(args[1]) == 0):
		# 	raise MissingArgument()

		pwd = self.db.getEntry(args[1], args[0])
		if (len(pwd) == 0):
			raise NotFound()
		clip.copy(self.db.getEntry(args[1], args[0]))
		print("Password Copied to Clipboard")

	# saves the account details to the database
	def save(self):
		args = list(self.flags.values())
		for x in args:
			if len(x) == 0:
				raise MissingArgument()

		self.db.addEntry(*args)
		print("Saved Successfully")

	# runs the program
	def run(self):
		try:
			if (len(sys.argv) < 2):
				raise SyntaxError()

			cmd = sys.argv[1]
			if (self.commands.get(cmd, '') == ''):
				raise SyntaxError()
			self.parse_flags()
			self.commands.get(cmd)()

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

