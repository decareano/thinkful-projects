# Snippets
# Garrett Anderson

import logging
import argparse
import sys
import json
import psycopg2


# Set the log outputfile and level
logging.basicConfig(filename="snippets.log", level = logging.DEBUG)

# Using json config file to avoid  uploading passwords to git, and dealing with different
# PostgreSQL usernames on different machines
logging.debug("Loading PostgreSQL connection config file")
try:
	with open("snippets_sqlconnection_config.json", 'r') as sqlcfg_file:
		sqlcfg = json.load(sqlcfg_file)
		sqlconnect_formatted_str = "dbname=\'%s\' user=\'%s\' password=\'%s\' host=\'%s\'" % (
			sqlcfg['dbname'],sqlcfg['user'],sqlcfg['password'],sqlcfg['host'],)

except:
	print "Error loading sql configuration file.  Please run sql_connection_config_script.py"
	sys.exit() # what should I do here?

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(sqlconnect_formatted_str)
logging.debug("Database connection established.")


def put(name, snippet):
	"""Store a snippet with an associated name."""
	logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
	cursor = connection.cursor()
	## Old way (see below for details)

	# try:
	# 	command = "insert into snippets values (%s, %s)"
	# 	cursor.execute(command, (name, snippet))
	# except psycopg2.IntegrityError as e:
	# 	# If already exists, rolls back changes and updates current entry
	# 	connection.rollback()
	# 	command = "update snippets set message=%s where keyword=%s"
	# 	cursor.execute(command, (snippet,name))
	# connection.commit()

	# New way.  Not sure if I did it right.  Don't understand what 'with' is doing
	try:
		with connection, connection.cursor() as cursor:
			command = "insert into snippets values (%s, %s)"
			cursor.execute(command, (name, snippet))
	except psycopg2.IntegrityError as e:
		with connection, connection.cursor() as cursor:
			command = "update snippets set message=%s where keyword=%s"
			cursor.execute(command, (name, snippet))




	logging.debug("Snippet stored successfully.")
	return name, snippet

def get(name):
	"""Retrieve the snippet with a given name."""
	logging.info("Retrieving snippet {!r}".format(name))
	## Old way, prone to error, exceptions, all kinds of cursor problems
	# cursor = connection.cursor()
	# cursor.execute("select message from snippets where keyword='%s'",(name,))
	# returnvalue = cursor.fetchone()
	# connection.commit()

	returnvalue = None # Set to none beforehand 
	# Better way to handle cursors: clean breaks, autocleanup, rollback, etc
	with connection, connection.cursor() as cursor:
		cursor.execute("select message from snippets where keyword=%s",(name,))
		returnvalue = cursor.fetchone()


	if not returnvalue:
		# No snippet found with that name
		# Prints error message, logs error, returns variable with None type,
		# which is further managed in if/else clause below in main function
		# for get subarg setup
		print("Snippet '{}'' not found".format(name))
		logging.debug("Snippet {!r} not found".format(name))
		return returnvalue
	logging.debug("Snippet retrieved successfully")
	return returnvalue[0]

def catalog():
	"""Returns a list of snippet names from database in alphabetical order"""
	logging.debug("Catalog(): Querying all names from snippets database")
	with connection, connection.cursor() as cursor:
		cursor.execute("SELECT keyword FROM snippets order by keyword")
		fetchall = cursor.fetchall()
	if not fetchall:
		# Nothing in catalog
		print "Nothing in snippets catalog.  Please add snippets with 'put' command."
		logging.debug("Catalog empty, returning None.")
		return None
	else:
		catalog = [x[0] for x in fetchall]
		logging.debug("Returning keywords in catalog database")
		return catalog

def search(query):
	"""Returns snippet names and text for search query"""
	logging.debug("search(): searching names and snippets for query string")


	with connection, connection.cursor() as cursor:
		command = "SELECT * FROM snippets where keyword like \'%%%s%%\' or message like \'%%%s%%\'" % (query, query)
		cursor.execute(command)
		fetchall = cursor.fetchall()
	if not fetchall:
		print "No queries found.  Please try another search."
		logging.debug("Search empty, returning None.")
		return None, None 
	else:
		name, message = [x[0] for x in fetchall], [x[1] for x in fetchall]
		logging.debug("Returning keywords in catalog database")
		return name, message


def main():
	"""Main function."""
	logging.info("Constructing parser.")
	parser = argparse.ArgumentParser(description="Store and retrieve snippets of text.")
	
	subparsers = parser.add_subparsers(dest="command", help="Available commands")

	# Subparser for put command
	logging.debug("Constructing put subparser.")
	put_parser = subparsers.add_parser("put", help="Store a snippet.")
	put_parser.add_argument("name", help="The name of the snippet.")
	put_parser.add_argument("snippet", help="The Snippet text.")
	
	# Subparser for get command
	logging.debug("Constructing get subparser.")
	get_parser = subparsers.add_parser("get", help="Return a snippet.")
	get_parser.add_argument("name", help="The name of the snippet.")

	# Subparser for catalog
	logging.debug("Constructing catalog subparser.")
	catalog_parser = subparsers.add_parser("catalog", help="Returns list of snippet names.")
	
	# Subparser for search
	logging.debug("Constructing search subparser.")
	search_parser = subparsers.add_parser("search", help="Returns list of snippets that matches search query.")
	search_parser.add_argument("query", help="The search string,preferably in quotes")


	arguments = parser.parse_args(sys.argv[1:])
	# Converts parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	command = arguments.pop("command")

	if command == "put":
		name, snippet = put(**arguments)
		print("Stored {!r} as {!r}.".format(snippet, name))
	elif command == "get":
		# import pdb; pdb.set_trace() # pdb debug starting here
		snippet = get(**arguments)
		if snippet != None:
			print("Retrieved snippet: {!r}.".format(snippet))
		else:
			print "Error retrieving snippet."
	elif command == "catalog":
		keywords = []
		keywords = catalog()
		if len(keywords) != 0:
			print "Keywords found in snippets database:"
			for keyword in keywords:
				print keyword
		else:
			print "Database empty.  No keywords found."
	elif command == "search":

		name, message = search(**arguments)
		if name != None:
			print "Returning list of keywords and snippets that match search query."
			name_message_list = [(name, message)]
			print "Keyword:           Message"
			for n,m in name_message_list:
				print("{}: {}".format(n,m))
		elif name == None:
			"No search query found."
		

if __name__ == '__main__':
	main()