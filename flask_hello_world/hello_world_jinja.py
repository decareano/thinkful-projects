from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def index():
	return render_template('template.html', mystring = "Home Page")

@app.route("/hello")
def hello():
	return render_template('template.html', mystring = "Hello World!")
	# return "Hello World!"

@app.route("/hello/<name>")
def hello_person_name(name):
	return render_template('template.html', mystring="Hello, " + name)
	# return "Hello {}!".format(name.title())

@app.route("/jedi/<fname>/<lname>")
def jedi(fname, lname):
	jediname = lname[:3]+fname[:2]
	return render_template('template.html', 
		mystring = "Your Jedi name is: {}".format(jediname),
		)
	# return "Your Jedi name is: {}".format(jediname.title())

@app.template_filter()
def jedi_name(fname, lname):
	return (lname[:3] + fname[:2]).title()


if __name__ == '__main__':
	app.run(debug=True)
