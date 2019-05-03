from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Creates an instance of Flask
app = Flask(__name__)

# Uses PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

# # Finds one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

# # Returns template and data
    return render_template("index.html", mars_data=mars_data)

# Route that triggers the scrape function
@app.route("/scrape")
def scrape():

# # Runs the scrape function and save the results to a variable
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)

# # Redirects back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)