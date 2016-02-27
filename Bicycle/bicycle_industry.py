# The Bicycle App
# By Garrett Anderson

import random

class Bicycle(object):
	"""The Bike Class"""
	def __init__(self, model, weight, cost):
		self.model = model
		self.weight = float(weight)
		self.cost = round(float(cost), 2)

class BikeShop(object):
	"""The Shop Class (HA! GET IT?!?!? Meh.)"""
	def __init__(self, name):
		self.name = name
		self.inventory = ()
		self.profit = 0

	def sell_bike(self, inventory_index, retail_margin):
		del self.inventory[inventory_index]
		self.profit += retail_margin * self.profit
	def return_profit(self):
		return self.profit

class Customer(object):
	"""My Boss says they're always right.  I think they're both not right in the head."""
	def __init__(self, name, cash):
		
		self.name = name
		self.cash = round(float(cash), 2)
		self.bikes = []

def print_customer_affordability(customers, shop):
	inventory = {}
	for bike in shop.inventory:
		inventory[bike.model] = bike.cost
	# print "list inventory: ", inventory

	print "A list of customers, and what bikes they can afford at %s." % (shop.name)
	for schmoe in customers:
		for x,y in inventory.iteritems():
			if y <= schmoe.cash: print "%s can afford a %s for $%i." % (schmoe.name, x, y)

def print_shop_inventory(shop):
	inventory = {}
	for bike in shop.inventory:
		inventory[bike.model] = bike.cost
	print "Inventory for shop %s:" % (shop.name)
	for model,cost in inventory.iteritems():
		print "Bike model %s at initial cost of $%i." % (model, cost)



def main():
	# I created the bike shop.  That's my name.  You can't use it.
	bikeshop1 = BikeShop('I Bike Your Pardon')
	bikeshop1.profit = 0.2

	bike_brands = ['Trek', 'Salsa', 'Jamis', 'Specialized', 'Surly', 'Giant', 'Bianchi',
	'Cannondale', 'Soma', 'Cervelo']
	bikes = []
	for x in xrange(7):
		bikebrand = random.choice(bike_brands)
		bikeweight = random.randint(19,23) # in lbs, unfortunately.  GO METRIC!
		bikecost = random.randint(100,1200)
		bikes.append(Bicycle(bikebrand,bikeweight,bikecost)) 
	bikeshop1.inventory = [x for x in bikes]

	Mike = Customer('Mike', 200)
	Joe = Customer('Joe', 500)
	Sam = Customer('Sam', 1000)
	customers = [Mike, Joe, Sam]

	print_customer_affordability(customers, bikeshop1)
	# print_shop_inventory(bikeshop1)


main()






		
