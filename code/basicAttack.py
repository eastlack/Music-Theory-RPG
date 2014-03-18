import sys

class BasicAttack(object):
	def __init__(self, name, power, description):
		self.name = name
		self.power = power
		self.description = description

	# return accuracy modifier based on user input
	# be sure to make it actually do that in the near future
	def calcAccuracy(self):
		return 1.0
