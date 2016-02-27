# Your friendly neightborhood bartender, mixing up exactly what you need
# Garrett Anderson

import random

class Bartender(object):
	"""Your friendly Python bartender!"""
	def __init__(self):

		self.questions = {
		"strong":"You looking for a stiff one?",
		"sweet":"You like it sweet?",
		"bitter":"You need something bitter?",
		"rock":"Straight up or on the rock?",
		"fruity":"Do you need your serving of fruit today?",
		}
		self.ingredients = {
		"strong":["Bourbon"],
		"sweet":["Simple Syrup", "Muddled demerara sugar cube"],
		"bitter":["Angostura bitters"],
		"rock":["Large, single ice cube."],
		"fruity":["Flamed Orange Peel","Luxardo Cherries"]
		}

	def ask_questions(self):
		self.answers = {}
		yes = ['yes', 'y']
		no = ['no','n']
		for x,q in self.questions.iteritems():
			while True:
				print q
				answer = raw_input("Yes or No? (Y or N)> ").lower()
				if answer in yes: 
					answer = True
					break
				elif answer in no:
					answer = False
					break
				else:
					print "I do not understand."
			self.answers[x] = answer
			print self.answers

	def construct_perfect_drink(self):
		drink_ingredients = []
		# I don't care if they answered true or false, they're getting an Old Fashioned
		for x in self.questions.keys():
			ingredient = random.choice(self.ingredients[x])
			print ingredient

		print "Congratulations, you have a fine Old Fashioned there,"
		print "(the only cocktail allowed in my bar.  This is a class joint.)"


def main():
	bartender = Bartender()
	bartender.ask_questions()
	bartender.construct_perfect_drink()

if __name__ == '__main__':
	main()