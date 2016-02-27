from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
	"""Convert a datetime to a different format"""
	return value.strftime(format)

@app.route("/")
def template_test():
	return render_template(
		'template.html', 
		my_string = "Wheeeee!",
		my_list= [x for x in range (11)],
		current_time = datetime.datetime.now())

@app.route("/home")
def home():
	return render_template(
		'template.html',
		my_string = "I'm the home page",
		my_list=[x for x in range (6)])

@app.route("/about")
def about():
	return render_template(
		'template.html',
		my_string = "I'm the about page",
		my_list=[x for x in range (6)])

@app.route("/contact")
def contact():
	return render_template(
		'template.html',
		my_string = "I'm the contact page",
		my_list=[x for x in range (6)])

if __name__ == '__main__':
	app.run(debug=True, host="127.0.0.1", port=5000)
