from flask import Flask

app=Flask(__name__)

@app.route("/")
def index():
	return "Index Page"

@app.route("/hello")
def hello():
	return "Hello World!"

@app.route("/hello/<name>")
def hello_person_name(name):
	return "Hello {}!".format(name.title())

@app.route("/jedi/<fname>/<lname>")
def jedi(fname, lname):
	jediname = lname[:3]+fname[:2]
	return "Your Jedi name is: {}".format(jediname.title())



if __name__ == '__main__':
	app.run(debug=True)
