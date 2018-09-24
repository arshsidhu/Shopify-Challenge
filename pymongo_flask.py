from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "myStores"
app.config["MONGO_URI"] = "mongodb://localhost:27017/myStores"
mongo = PyMongo(app)

@app.route("/")
def Welcome():
	return "Welcome"

@app.route("/add")
def add():
	stores = mongo.db.Stores
	stores.insert({"name":"Walmart",
	 "orders":{},
	  "products":[{"name":"bread", "price":2.50}]})
	return "Store Added"

@app.route("/find")
def find():
	stores = mongo.db.Stores
	superstore = stores.find_one({"name":"Superstore"}) 
	return superstore["name"]

@app.route("/update")
def update():
	stores = mongo.db.Stores
	walmart = stores.find_one({"name":"Walmart"}) 
	walmart["products"][0]["name"] = "cheese"
	stores.save(walmart)
	return walmart["products"][0]["name"]

@app.route("/delete")
def delete():
	stores = mongo.db.Stores
	superstore = stores.find_one({"name":"Superstore"})
	stores.remove(superstore)
	return "removed " 

if __name__ == "__main__":
	app.run(debug=True)