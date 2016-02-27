import json
import getpass


# Using json config file to avoid  uploading passwords to git, and dealing with different
# PostgreSQL usernames on different machines

def main():
	print "Configuring PostgreSQL connection JSON config file."
	projectname = raw_input('Please enter project name.> ')
	db_name = raw_input('Please enter database name.> ')
	username = raw_input('Please enter db admin username.> ')
	password = getpass.getpass('Enter admin password:> ')
	host = raw_input("Please enter database host server (if local, type 'localhost' without quotes.> ")

	conf_dict = {
	"dbname" : db_name,
	"user": username,
	"password": password,
	"host":host
	}

	filename = "%s_sqlconnection_config.json" % (projectname)
	with open(filename, 'w') as cfg:
		cfg.write(json.dumps(conf_dict))

if __name__ == '__main__':
	main()

