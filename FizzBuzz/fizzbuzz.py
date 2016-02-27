import sys

def fizzbuzz(maxnum):
	print "Counting to %i." % (maxnum)
	for n in xrange(1,maxnum+1): # Generator object for counting numbers
		if n % 3 == 0 and n % 5 == 0:
			print "Fizz-Buzz!"
		elif n % 3 == 0:
			print "Fizz"
		elif n % 5 == 0:
			print "Buzz"
		else:
			print n

	def get_input(numstr):
		while True:
			if numstr.isdigit():
				return abs(int(numstr))
			else:
				numstr = raw_input('Numerical values ONLY, please. > ')

def main():
	if len(sys.argv) > 1:
		try:
			maxnum = abs(int(sys.argv[1]))
		except:
			numstr = sys.argv[1]
			maxnum = get_input(numstr)
	else:
		try:
			maxnum = abs(int(raw_input('Please enter the largest number to count to: ')))
		except:
			maxnum = get_input('numstr')

	fizzbuzz(maxnum)

if __name__ == "__main__":
	main()