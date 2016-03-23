import json
import getpass


# Using json config file to avoid  uploading passwords to git, and dealing with different
# PostgreSQL usernames on different machines

def main():
	secret_env_key = ""

	print("Configuring PostgreSQL connection JSON config file.")
	db_name = input('Please enter SQL database name.> ')
	username = input('Please enter db admin username.> ')
	password = getpass.getpass('Enter admin password:> ')
	host = input("Please enter database host server (leave blank for default localhost) > ")
	port = input("Please enter port number (leave blank for default port 5432.> ")
	if host == "": host = "localhost"
	if port == "": port = 5432


	conf_dict = {
	"dbname": db_name,
	"user": username,
	"password": password,
	"host": host,
	"port": port,
	"secret_key": secret_env_key,
	"server_ip": host
	}

	filename = "sqlconnection_config_%s.json" % (projectname)
	with open(filename, 'w') as cfg:
		cfg.write(json.dumps(conf_dict))

if __name__ == '__main__':
	main()

