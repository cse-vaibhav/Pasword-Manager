
class InvalidArgument(Exception):
	def err_msg(self):
		print("Invalid Argument.")

class SyntaxError(Exception):
	def err_msg(self):
		print("Incorrect Syntax.")

class MissingArgument(Exception):
	def err_msg(self):
		print("Missing Argument.\nTry 'pm help' for a list of available commands.")

class NotFound(Exception):
	def err_msg(self):
		print("No Entry Found.")
