import sqlite3 as sql
import os

class Database:
	
	def __init__(self):
		self.con = sql.connect('user.db')
		self.cur = self.con.cursor()
		self.cols = ["Username", "Site", "Password"]

		# Create table if it does not already exist
		if (not self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'").fetchone()):
			self.cur.execute("CREATE TABLE data(Username TEXT, Site TEXT, Password TEXT);")

	def save(self, uname, site, passwd):

		# Update entry if it already exists
		if (self.check(uname, site)):
			self.cur.execute(f"UPDATE data SET Password='{passwd}' WHERE Username='{uname}' AND Site='{site}';")
			self.con.commit()
			print("Password Updated.")
			return

		# Create a new entry otherwise
		self.cur.execute(f"INSERT INTO data (Username,Site,Password) VALUES('{uname}', '{site}', '{passwd}');")
		self.con.commit()
		print(f"Saved Password.")
		return

	def delete(self, uname, site):

		# Check if the entry exists or not
		if (not self.check(uname, site)):
			print("No Entry Found.")
			return

		# Delete the entry
		self.cur.execute(f"DELETE FROM data WHERE Username='{uname}' AND Site='{site}';")
		self.con.commit()
		print("Entry Deleted.")
		return

	def get(self, uname="", site=""):

		# Print all usernames and sites
		if (len(uname) == 0 and len(site) == 0):
			self.cur.execute("SELECT *FROM data;")
			print("\t".join(self.cols[:2]))
			for row in self.cur.fetchall():
				print(row[0], "\t\t", row[1])
			return

		# Check if corresponding entry exists or not
		if (not self.check(uname, site)):
			print("No Entry Found.")
			return

		# Copy the entry to the clipboard
		self.cur.execute(f"SELECT * FROM data WHERE Username='{uname}' AND Site='{site}';")
		return self.cur.fetchone()[2]

	def check(self, uname="", site=""):
		self.cur.execute(f"SELECT Username,Site FROM data WHERE Username='{uname}' AND Site='{site}'")
		if (len(self.cur.fetchall()) == 0):
			return False
		return True

	"""
	Have the function export data to formats other than csv.
	"""
	def export_data(self, path, fmt="csv"):

		# convert the path to absolute path before exporting
		path = os.path.join(os.path.abspath(path))
		with open(path, 'w') as file:
			file.write(",".join(self.cols))
			self.cur.execute("SELECT * FROM data;")
			for row in self.cur.fetchall():
				file.write('\n')
				file.write(",".join(list(row)))
		return

	"""
	Have the function import data from formats other than csv.
	"""
	def import_data(self, file_path, fmt="csv"):
		file_path = os.path.abspath(file_path)
		with open(file_path, 'r') as file:
			file.readline()
			for row in file.readlines():
				row = row.strip().split(',')
				self.save(*row)
		return

