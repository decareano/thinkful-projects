import random
import sys

# Better code, better algorithm, just plain better.
# Garrett Anderson j.garrett.anderson@gmail.com

class GuessingGame(object):
	"""Try to guess the number in the fewest tries!"""
	def __init__(self, minnum, maxnum, chooserandom):
		self.minnum = minnum
		self.maxnum = maxnum
		self.ceiling = maxnum
		self.floor = minnum
		padding = 100
		self.chooserandom = chooserandom
		self.theNumber = None

		if self.chooserandom == True:
			self.theNumber = self.select_random_number()

		self.currentguess = int(0.5 * (self.maxnum-self.minnum))



	def select_random_number(self):
		return random.randint(self.minnum, self.maxnum)


	def theDivider(self):
		# Chooses the middle number between the current ceiling and floor
		result = int(0.5 * (self.ceiling-self.floor))
		return result

	def startguessing(self):
		counter = 0
		usedscores = []

		while True:
			print "newguess", self.currentguess

			counter += 1
			usedscores.append(self.currentguess)
			# If winning number, it declares winner.  Otherwise it declares 
			# whether guess was higher or lower than TheNumber, then 
			# lowers ceiling or raises floor depending on result.  
			# Keeps a list of every guess.
			if self.currentguess == self.theNumber:
				print "You win with the #%i, in %i tries!" % (self.theNumber, counter)
				break

			elif self.currentguess < self.theNumber:
				print "Guessed wrong.  Currentguess is < TheNumber."
				self.floor = self.currentguess
				add_or_sub = self.theDivider()
				self.currentguess += add_or_sub

			elif self.currentguess > self.theNumber:
				print "Guessed wrong.  Currentguess is > TheNumber."
				self.ceiling = self.currentguess
				add_or_sub = self.theDivider()
				self.currentguess -= add_or_sub

			# Checks to see if current guess is in the list of previous guesses.
			# If it is, it raises or lowers it appropriately by one, usually to
			# get the final answer.
			if self.currentguess < self.theNumber: self.currentguess += 1
			if self.currentguess in usedscores and \
			self.currentguess > self.theNumber: self.currentguess -= 1

def main():
	# If player wants to play with user input, accepts The Number as the first argument
	# If no argument, or input not an integer, sets it to choose random numbers for you.

	argnumber = None
	playrandom = True

	if len(sys.argv) > 1:
		try:
			argnumber = abs(int(sys.argv[1]))
			playrandom = False
		except:
			print "I'm sorry, but only integers accepted as an argument."
			print "We shall play with a random number choosen instead."
			playrandom = True

	thegame = GuessingGame(0, 100, playrandom)
	if argnumber != None:
		thegame.theNumber = argnumber
	print "The Number is: ", thegame.theNumber
	thegame.startguessing()

if __name__ == '__main__':
	main()