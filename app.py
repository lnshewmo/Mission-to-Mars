# mission to mars app.py
# by Laura Miller

#use flask - render a template, redirect to another url and create a url
from flask import Flask, render_template, redirect, url_for
# PyMongo interacts with the Mongo DB
from flask_pymongo import PyMongo
# to use the scraping code, convert from Jup to python
import scraping

# setup Flask
app = Flask(__name__)

# use flask pymongo to setup mongo connection
# uniform resourse identifier URI
# app will reach mongo thru localhost server using port 27017, using mars_app db
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# setup routes for the html page
@app.route("/")
# index is home page
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# setup scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
	app.run(debug=True)