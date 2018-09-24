# Arshdeep Sidhu
# Shopify challenge Winter 2019
from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo

app = Flask(__name__)
# Connects to db hosted via MLabs
app.config["MONGO_DBNAME"] = "shopify-challenge"
app.config["MONGO_URI"] = "mongodb://User:Password1@ds235788.mlab.com:35788/shopify-challenge"
mongo = PyMongo(app)

#Home route, displays all the stores by name
@app.route("/")
def Welcome():
	welcomeStr = "Welcome :)\nList of stores: \n\n"
	
	for post in mongo.db.Stores.find():
		welcomeStr += post["name"] + "\n"
	return welcomeStr

#Store front route, displays all products in a store
@app.route("/<string:storeName>")
def showProducts(storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	productsInStore = selectedStore["products"]
	products = ""
	
	for prod in productsInStore:
		products += prod["name"] + "---$" + str(prod["price"]) + "\n"
	
	return products

#Route to show all the orders in a specific store
@app.route("/<string:storeName>_orders")
def showOrder(storeName):
	orderStr = ""
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	orderObj = selectedStore["orders"]
	
	for order in orderObj:
		orderNum = order["orderNum"]
		totOrderPrice = order["totPrice"]
		prodInOrder = order["productsInOrder"]
		orderStr += "Order Number: " + str(orderNum) + "\n"
		
		for prod in prodInOrder:
			orderStr += prod["name"] + "---$" + str(prod["price"]) + "---Amount:" +str(prod["amount"]) + "\n"
		orderStr += "-------------\nTotal price: " + str(totOrderPrice) + "\n\n"
	
	return orderStr

#Route to show a specific order in a specific store
@app.route("/<string:storeName>_order_number_<int:num>")
def showSpecificOrder(storeName, num):
	orderStr = ""
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	orderObj = selectedStore["orders"]
	selectedOrder = orderObj[num-1]
	totOrderPrice = selectedOrder["totPrice"]
	orderNum = selectedOrder["orderNum"]
	prodInOrder = selectedOrder["productsInOrder"]
	orderStr += "Order Number: " + str(orderNum) + "\n"
	
	for prod in prodInOrder:
		orderStr += prod["name"] + "---$" + str(prod["price"]) + "---Amount:" +str(prod["amount"]) + "\n"
	
	orderStr += "-------------\nTotal price: " + str(totOrderPrice) + "\n\n"	
	return orderStr

#Route to delete an entire store
@app.route("/delete_<string:storeName>")
def deleteStore(storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	stores.remove(selectedStore)
	
	return storeName + " was removed"

#Route to delete all orders in a store
@app.route("/delete_<string:storeName>/all_orders")
def deleteAllOrders(storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	selectedStore["orders"] = []
	stores.save(selectedStore)
	
	return "All orders in " + storeName +" have been removed"

#Route to delete a specific order in a store
@app.route("/delete_<string:storeName>/order_number_<int:num>")
def deleteOneOrder(storeName, num):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	selectedStore["orders"].pop(num-1)
	
	for x in range(num-1, len(selectedStore["orders"])):
		selectedStore["orders"][x]["orderNum"] -= 1
	
	stores.save(selectedStore)
	return "Order number " + str(num) + " was deleted from store " + storeName 

#Route to delete a product from a store
@app.route("/delete_<string:storeName>/product_<string:prodName>")
def deleteProduct(storeName, prodName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	
	for prod in selectedStore["products"]:
		if (prod["name"] == prodName):
			selectedStore["products"].remove(prod)
			break
	
	stores.save(selectedStore)
	return "Product " + prodName + " was removed from store " + storeName

#Route to delete a product from a specific order
@app.route("/delete_<string:storeName>/order_number_<int:num>/product_<string:prodName>")
def deleteOrderProduct(storeName, num, prodName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	deletedPrice = 0
	
	for prod in selectedStore["orders"][num]["productsInOrder"]:
		if (prod["name"] == prodName):
			deletedPrice = prod["price"]
			if(prod["amount"] == 1):
				selectedStore["orders"][num]["productsInOrder"].remove(prod)
			else:
				prod["amount"] -= 1
			break
	
	selectedStore["orders"][num]["totPrice"] -= deletedPrice
	stores.save(selectedStore)
	return "Product " + prodName + " was deleted from order number " + str(num) + " from the store, " + storeName

#Route to add a store, without any products or orders
@app.route("/add_store_<string:storeName>")
def addStore(storeName): 
	mongo.db.Stores.insert({"name":storeName, "orders":[], "products":[]})
	
	return storeName + " added"

#Route to add a product to a store
@app.route("/add_<string:product>_<float:price>/<string:storeName>")
def addProductToStore(product, price, storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	prodJson = {"name":product, "price":price}
	selectedStore["products"].append(prodJson)
	stores.save(selectedStore)
	
	return product + " added to " + storeName

#Route to start a new order, adds a new product to that order
@app.route("/<string:storeName>/add_to_order/<string:product>")
def addToOrder(storeName, product):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	orders = selectedStore["orders"]
	prodObj = {}
	
	for prod in selectedStore["products"]:
		if (prod["name"] == product):
			prodObj = prod
	prodObj["amount"]=1
	orderObj = {"orderNum":len(orders)+1,
				"totPrice":prodObj["price"],
				"productsInOrder":[prodObj]}
	selectedStore["orders"].append(orderObj)
	stores.save(selectedStore)
	
	return "New order started in "+storeName+"!\n"+product+" added to order"

#Adds product to an existing order
@app.route("/<string:storeName>/add_to_order_number_<int:num>/<string:product>")
def addToSpecificOrder(storeName, num, product):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	order = selectedStore["orders"][num-1]
	prodObj = {}
	
	for prod in selectedStore["products"]:
		if (prod["name"] == product):
			prodObj = prod
	
	for prod in selectedStore["orders"][num-1]["productsInOrder"]:
		if (prod["name"] == prodObj["name"]):
			prod["amount"] += 1
			selectedStore["orders"][num-1]["totPrice"] += prodObj["price"]
			stores.save(selectedStore)
			return product + " added to order number " + str(num) + " in "+ storeName
	
	prodObj["amount"] = 1
	selectedStore["orders"][num-1]["productsInOrder"].append(prodObj)
	selectedStore["orders"][num-1]["totPrice"] += prodObj["price"]
	stores.save(selectedStore)
	
	return product + " added to order number " + str(num) + " in "+ storeName

#Adds store via json and POST request. 
@app.route("/add_store", methods=["POST"])
def addStoreViaJSON():
	stores = mongo.db.Stores
	
	if (request.method == "POST"):
		inpJson = request.get_json()
		stores.insert(inpJson)
		return "added store: " + inpJson["name"]
	else:
		return "invalid JSON:"

#Adds order to a specific store via json and POST request
@app.route("/<string:storeName>/add_order", methods=["POST"])
def addOrderViaJSON(storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	orderObj = {}
	orderNum = 0
	totOrderPrice = 0
	
	if (request.method == "POST"):
		inpJson = request.get_json()
		
		for prod in inpJson["order"]:
			if(prod["amount"] == 1):
				totOrderPrice += prod["price"]
			else:
				for x in range(0,prod["amount"]):
					totOrderPrice += prod["price"]

		orderNum = len(selectedStore["orders"]) + 1
		orderObj = {
		"orderNum":orderNum,
		"totPrice":totOrderPrice,
		"productsInOrder":inpJson["order"]
		}
		selectedStore["orders"].append(orderObj)
		stores.save(selectedStore)

		return jsonify({"order added: ": inpJson}), 201
	else:
		return "invalid JSON"

#Adds products to a store via json and POST request
@app.route("/<string:storeName>/add_products", methods=["POST"])
def addProductsViaJSON(storeName):
	stores = mongo.db.Stores
	selectedStore = stores.find_one({"name":storeName})
	
	if (request.method == "POST"):
		inpJson = request.get_json()
		stores.save(selectedStore)
		
		for prod in inpJson["products"]:
			selectedStore["products"].append(prod)
		
		return jsonify({"products added: ": inpJson}), 201
	else:
		return "invalid JSON"
		
#Method allows for the use of new line characters while displaying information
@app.after_request
def treat_as_plain_text(response):
    response.headers["content-type"] = "text/plain"
    return response

if __name__ == "__main__":
	app.run(debug=True)