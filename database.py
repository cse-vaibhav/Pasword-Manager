from error import *
from collections import defaultdict
import pickle
import os

class Database:
	def __init__(self):
		self.data = defaultdict(defaultdict)

	def addEntry(self, username, site, pwd):
		self.data[username][site] = pwd
		self.data[site][username] = pwd

	def checkEntry(self, username, site):
		if (len(username) == 0 or len(site) == 0):
			return False
		try:
			self.data[username][site]
			self.data[site[username]]
			return True
		except KeyError:
			raise NotFound()

	def deleteEntry(self, username, site):
		if self.checkEntry(username, site):
			del self.data[username][site]
			del self.data[site][username]

	def getEntry(self, username = '', site = ''):

		try:
			if (not self.checkEntry(username, site)):
				raise NotFound()
			if (0 in [len(username), len(site)]):
				if (len(username) == 0):
					keys = self.data[site].keys()
				elif (len(site) == 0):
					keys = self.data[site].keys()

				for x in range(1, len(keys)+1):
					print(f"{x} {keys[x-1]}")

				idx = int(input("choose from the given options: ").strip(' '))
				if (idx not in range(1, len(keys)+1)):
					raise InvalidArgument()

				if (len(username) == 0):
					username = keys[idx-1]
				elif (len(site) == 0):
					site = keys[idx-1]
			return self.data[site][username]
		except:
			raise NotFound()

	def save(self):
		with open("pass.pkl", 'wb') as db:
			pickle.dump(self.data, db)

	def load(self):
		with open("pass.pkl", 'rb') as db:
			try:
				self.data = pickle.load(db)
			except:
				return
				
	# def to_csv(self, path):
	# 	with open(f"{os.path.join([path, 'data.csv'])}", "w") as expData:
	# 		x = defaultdict(defaultdict)
	# 		expData.write("Usernames, Webiste, PassWord")
	# 		for k, v in self.data.items():


	# 		pass

