#!/usr/bin/env -S python3
from database import *
from error import *
import clipboard as clip
import sys
import os
import logging
from pprint import pprint 


logging.disable()
logging.basicConfig(filename="logs.log",filemode="w", level=logging.DEBUG)

class PasswordManager:
	def __init__(self):
		self.db = Database()

		self.commands = {
			"help" : self.help,
			"save" : self.save,
			"get" : self.get,
			"list" : self.list,
			"delete" : self.delete,
			"import" : self.import_csv,
			"export" : self.export_csv
		}

	def import_csv(self, path=''):
		self.db.import_data(sys.argv[2]);
		return

	def export_csv(self, path=''):
		self.db.export_data(sys.argv[2]);
		return
	
	# prints the help message
	def help(self):
		print("""
		pm is a command-line utility to stores and ret11rieves all your passwords.

		Commands:

		help\t\t-\tshows this help page.
		get\t\t-\tcopies the password to the clipboard.
		save\t\t-\tsave or update password.
		delete\t\t-\tdeletes an entry.
		export\t\t-\texport your data to a csv file
		import\t\t-\timport your data from a csv file
		list \t\t-\tlists all users and sites stored.

		Flags:

		-s\t\t-\tspecifies that argument given is a website.
		-u\t-\tspecifies that argument given is a username or email.
		-p\t\t-\tspecifiers that argument given is a password.

		""")

	# parses the email, password and username in the given arguments
	def parse_flags(self):
		# returns the index of arg in args and if not found returns -1
		def index(args, arg):
			try:
				return args.index(arg)
			except ValueError:
				return -1

		# flags
		flgList = ["-s", "-u", "-p"]
		args = sys.argv[1:]
		self.flags = {x : "" for x in flgList}
		for flag in flgList:
			if index(args, flag) >= 0:
				self.flags[flag] = args[index(args, flag)+1]

	# deletes an entry
	def delete(self):
		args = list(self.flags.values())
		self.db.delete(args[1], args[0])
		print("Deleted Successfully")

	# copies the password to clipboard
	def get(self):
		args = list(self.flags.values())
		if (len(args[0]) == 0 or len(args[1]) == 0):
			raise MissingArgument()

		pwd = self.db.get(args[1], args[0])
		if (len(pwd) == 0):
			raise NotFound()
		clip.copy(pwd)
		print("Password Copied to Clipboard")

	# save the details
	def save(self):
		args = list(self.flags.values())
		for arg in args:
			if len(arg) == 0:
				raise missingargument()

		self.db.save(args[1], args[0], args[2])

	def list(self):
		cur = self.db.cur
		cur.execute("SELECT Username,Site FROM data;")
		print("Username\tSite")
		for u, s in cur.fetchall():
			print(f"{u}\t{s}")

	def run(self):
		try:
			if (len(sys.argv) < 2):
				raise MissingArgument()

			# cmd = sys.argv[1]
			cmd = self.commands.get(sys.argv[1], None)
			if (cmd is None):
				raise MissingArgument()
			self.parse_flags()
			cmd()

		except Exception as e:
			e.err_msg()

if __name__ == "__main__":

	app = PasswordManager()
	app.run()
