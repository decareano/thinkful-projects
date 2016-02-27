from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Table, Integer, Float, String, DateTime, Date, ForeignKey
import json
import logging
import sys

logging.basicConfig(filename="tbay.log", level = logging.DEBUG)

logging.debug("Loading PostgreSQL connection config file")
try:
	with open("sqlconnection_config_tbay.json", 'r') as sqlcfg_file:
		sqlcfg = json.load(sqlcfg_file)
		sqlconnect_formatted_str = "postgresql://%s:%s@%s:%s/%s" % (
			sqlcfg['user'],sqlcfg['password'],sqlcfg['host'],sqlcfg['port'], sqlcfg['dbname'],)

except:
	print("Error loading sql configuration file.  Please run sql_connection_config_script.py")
	logging.debug("Error loading sql configuration .json file.")
	sys.exit()


logging.debug("Initializing sqlalchemy engine")
try:
	engine = create_engine(sqlconnect_formatted_str)
	Session = sessionmaker(bind=engine)
	session = Session()
	Base = declarative_base()
except Exception as e:
	print("Error connecting.  Please check server settings.")
	print(e)
	logging.debug("Connection to PostgreSQL server failed, {!r}.".format(e))
	sys.exit()

logging.debug("sqlalchemy engine initialized.")


#########
logging.debug("Init auction intermediate association table")
bid_item_table = Table('bid_item_association', Base.metadata,
	Column('user_id', Integer, ForeignKey('users.id')),
	Column('item_id', Integer, ForeignKey('items.id')),
	Column('bid_id', Integer, ForeignKey('bids.id'))
	)



logging.debug("Init Base class Item")
class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	description = Column(String)
	start_time = Column(DateTime, default = datetime.utcnow)

	owner_id = Column(Integer, ForeignKey('users.id'), nullable = False)
	bids = relationship("Bid")
	# bids = relationship("Bid", secondary="bid_item_association", backref = "item", uselist = False)

logging.debug("Init Base class User")
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	username = Column(String, nullable = False)
	password = Column(String, nullable = False)

	items = relationship("Item", backref = "owner")
	bids = relationship("Bid")
	# bids = relationship("Bid", secondary="bid_item_association", backref="user", uselist = False)

logging.debug("Init Base class Bid")
class Bid(Base):
	__tablename__ = "bids"
	id = Column(Integer, primary_key = True)
	price = Column(Float, nullable = False)

	user = relationship("User", uselist = False)
	item = relationship("Item", uselist = False)

	item_id = Column(Integer, ForeignKey('items.id'), nullable = False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable = False)


##
logging.debug("Creating SQLAlchemy database class schema")
try:
	Base.metadata.create_all(engine)
except Exception as e:
	print("Error creating SQLAlchemy database class schema.")
	print("Error: ", e)
	logging.debug("Error creating SQLAlchemy database class schema, error {!r}".format(e))
	sys.exit()


#############
# Be sure to comment out the following if importing to ipython for testing,
# otherwise all these names and items will be duplicated upon import
logging.debug("Create user objects")
try:
	bob = User(username = "bob", password = "asdf")
	tim = User(username = "tim", password = "asdf")
	jake = User(username = "jake", password = "asdf")
	users = [bob, tim, jake]
	list(map(session.add, users)) # cool functional programming unpacking trick.  Read about later
	session.commit()
except Exception as e:
	print("Could not create user objects, error ", e)
	logging.debug("Error creating user objects, error {!r}".format(e))

logging.debug("Create item objects")
try:
	baseball = Item(name = "baseball", description = "Its a baseball.")
	bat = Item(name = "bat", description = "Its a bat.  For baseballs.")
	mitt = Item(name = "mitt", description = "Its a mitt.  For catching.  Baseballs.")
	bob.items.append(baseball)
	tim.items.append(bat)
	jake.items.append(mitt)
	items = [baseball, bat, mitt]

	list(map(session.add, items))
	session.commit()
except Exception as e:
	print("Could not create item objects, error ", e)
	logging.debug("Error creating item objects, error {!r}".format(e))

	# Be sure to comment out the following if importing script to ipython,
	# otherwise it will add another bid object
logging.debug("Create bid objects")
try:
	tim = session.query(User).filter(User.username=="tim").all()[0]
	jake = session.query(User).filter(User.username=="jake").all()[0]
	baseball = session.query(Item).filter(Item.name=="baseball").all()[0]
	timbid1 = Bid(price = 10, user = tim, item=baseball) 
	jakebid1 = Bid(price = 30, user = jake, item=baseball) 
	session.add(timbid1, jakebid1)
	session.commit()
except Exception as e:
	print("Bid commit failed")
	print("Error: ", e)
	sys.exit()

logging.debug("Test database objects via sqlalchemy queries")
try:
	tim = session.query(User).filter(User.username=="tim").all()[0]
	baseball = session.query(Item).filter(Item.name=="baseball").all()[0]
	firstbid = session.query(Bid).first()
	# Pay attention to what you did here.  Sorted list by object baseball.bids[x].price
	baseball_sorted = sorted(baseball.bids, key=lambda x: x.price, reverse=True)
	# largestbid = session.query.get(baseball.id).bids
	print("First bid: ", firstbid)
	print("First bid user, item names: " + firstbid.user.username +"," + firstbid.item.name)
	print("Tim's bids: ", tim.bids)
	print("All bids on baseball item: ", baseball.bids)
	print("User {} entered the highest bid on the baseball at ${}.".format(
		baseball_sorted[0].user.username,
		baseball_sorted[0].price))
except Exception as e:
	print("Queries failed")
	print("Error: ", e)
	sys.exit()


# # Returns a list of all of the user objects
# session.query(User).all() # Returns a list of all of the user objects

# # Returns the first user
# session.query(User).first()

# # Finds the user with the primary key equal to 1
# session.query(User).get(1)

# # Returns a list of all of the usernames in ascending order
# session.query(User.username).order_by(User.username).all()

# # Returns the description of all of the basesballs
# session.query(Item.description).filter(Item.name == "baseball").all()

# # Return the item id and description for all baseballs which were created in the past.  Remember to import the datetime object: from datetime import datetime
# session.query(Item.id, Item.description).filter(Item.name == "baseball", Item.start_time < datetime.utcnow()).all()

# allitems = session.query(Item).all()
# for item in allitems:
# 	session.delete(item)
# 	session.commit()



