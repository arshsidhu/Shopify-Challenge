# Arshdeep Sidhu
# Shopify challenge Winter 2019
from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo

app = Flask(__name__)
# Connects to db hosted via MLabs
app.config["MONGO_DBNAME"] = "shopify-challenge"
app.config["MONGO_URI"] = "mongodb://User:Password1@ds235788.mlab.com:35788/shopify-challenge"
mongo = PyMongo(app)

# Home route, displays all the stores by name
@app.route("/")
def Welcome():
	welcome_string = "Welcome :)\nList of stores: \n\n"
	
	for post in mongo.db.Stores.find():
		welcome_string += post["name"] + "\n"
	return welcome_string

# Store front route, displays all products in a store
@app.route("/<string:storeName>")
def showProducts(storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	products_in_store = selected_store["products"]
	products = ""
	
	for prod in products_in_store:
		products += prod["name"] + "---$" + str(prod["price"]) + "\n"
	
	return products

# Route to show all the orders in a specific store
@app.route("/<string:storeName>_orders")
def showOrder(storeName):
	order_string = ""
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	order_object = selected_store["orders"]
	
	for order in order_object:
		order_number = order["orderNum"]
		total_order_price = order["totPrice"]
		products_in_order = order["productsInOrder"]
		order_string += "Order Number: " + str(order_number) + "\n"
		
		for prod in products_in_order:
			order_string += prod["name"] + "---$" + str(prod["price"]) + "---Amount:" +str(prod["amount"]) + "\n"
		order_string += "-------------\nTotal price: " + str(total_order_price) + "\n\n"
	
	return order_string

# Route to show a specific order in a specific store
@app.route("/<string:storeName>_order_number_<int:num>")
def showSpecificOrder(storeName, num):
	order_string = ""
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	order_object = selected_store["orders"]
	selected_order = order_object[num-1]
	total_order_price = selected_order["totPrice"]
	order_number = selected_order["orderNum"]
	products_in_order = selected_order["productsInOrder"]
	order_string += "Order Number: " + str(order_number) + "\n"
	
	for prod in products_in_order:
		order_string += prod["name"] + "---$" + str(prod["price"]) + "---Amount:" +str(prod["amount"]) + "\n"
	
	order_string += "-------------\nTotal price: " + str(total_order_price) + "\n\n"	
	return order_string

# Route to delete an entire store
@app.route("/delete_<string:storeName>")
def deleteStore(storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	stores.remove(selected_store)
	
	return storeName + " was removed"

# Route to delete all orders in a store
@app.route("/delete_<string:storeName>/all_orders")
def deleteAllOrders(storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	selected_store["orders"] = []
	stores.save(selected_store)
	
	return "All orders in " + storeName +" have been removed"

# Route to delete a specific order in a store
@app.route("/delete_<string:storeName>/order_number_<int:num>")
def deleteOneOrder(storeName, num):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	selected_store["orders"].pop(num-1)
	
	for x in range(num-1, len(selected_store["orders"])):
		selected_store["orders"][x]["orderNum"] -= 1
	
	stores.save(selected_store)
	return "Order number " + str(num) + " was deleted from store " + storeName 

# Route to delete a product from a store
@app.route("/delete_<string:storeName>/product_<string:prodName>")
def deleteProduct(storeName, prodName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	
	for prod in selected_store["products"]:
		if (prod["name"] == prodName):
			selected_store["products"].remove(prod)
			break
	
	stores.save(selected_store)
	return "Product " + prodName + " was removed from store " + storeName

# Route to delete a product from a specific order
@app.route("/delete_<string:storeName>/order_number_<int:num>/product_<string:prodName>")
def deleteOrderProduct(storeName, num, prodName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	deleted_price = 0
	
	for prod in selected_store["orders"][num-1]["productsInOrder"]:
		if (prod["name"] == prodName):
			deleted_price = prod["price"]
			if(prod["amount"] == 1):
				selected_store["orders"][num-1]["productsInOrder"].remove(prod)
			else:
				prod["amount"] -= 1
			break
	
	selected_store["orders"][num-1]["totPrice"] -= deleted_price
	stores.save(selected_store)
	return "Product " + prodName + " was deleted from order number " + str(num) + " from the store, " + storeName

# Route to add a store, without any products or orders
@app.route("/add_store_<string:storeName>")
def addStore(storeName): 
	mongo.db.Stores.insert({"name":storeName, "orders":[], "products":[]})
	
	return storeName + " added"

# Route to add a product to a store
@app.route("/add_<string:product>_<float:price>/<string:storeName>")
def addProductToStore(product, price, storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	product_json = {"name":product, "price":price}
	selected_store["products"].append(product_json)
	stores.save(selected_store)
	
	return product + " added to " + storeName

# Route to start a new order, adds a new product to that order
@app.route("/<string:storeName>/add_to_order/<string:product>")
def addToOrder(storeName, product):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	orders = selected_store["orders"]
	product_object = {}
	
	for prod in selected_store["products"]:
		if (prod["name"] == product):
			product_object = prod
	product_object["amount"]=1
	order_object = {"orderNum":len(orders)+1,
				"totPrice":product_object["price"],
				"productsInOrder":[product_object]}
	selected_store["orders"].append(order_object)
	stores.save(selected_store)
	
	return "New order started in "+storeName+"!\n"+product+" added to order"

# Adds product to an existing order
@app.route("/<string:storeName>/add_to_order_number_<int:num>/<string:product>")
def addToSpecificOrder(storeName, num, product):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	order = selected_store["orders"][num-1]
	product_object = {}
	
	for prod in selected_store["products"]:
		if (prod["name"] == product):
			product_object = prod
	
	for prod in selected_store["orders"][num-1]["productsInOrder"]:
		if (prod["name"] == product_object["name"]):
			prod["amount"] += 1
			selected_store["orders"][num-1]["totPrice"] += product_object["price"]
			stores.save(selected_store)
			return product + " added to order number " + str(num) + " in "+ storeName
	
	product_object["amount"] = 1
	selected_store["orders"][num-1]["productsInOrder"].append(product_object)
	selected_store["orders"][num-1]["totPrice"] += product_object["price"]
	stores.save(selected_store)
	
	return product + " added to order number " + str(num) + " in "+ storeName

# Adds store via json and POST request. 
@app.route("/add_store", methods=["POST"])
def addStoreViaJSON():
	stores = mongo.db.Stores
	
	if (request.method == "POST"):
		input_json = request.get_json()
		stores.insert(input_json)
		return "added store: " + input_json["name"]
	else:
		return "invalid JSON:"

# Adds order to a specific store via json and POST request
@app.route("/<string:storeName>/add_order", methods=["POST"])
def addOrderViaJSON(storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	order_object = {}
	order_number = 0
	total_order_price = 0
	
	if (request.method == "POST"):
		input_json = request.get_json()
		
		for prod in input_json["order"]:
			if(prod["amount"] == 1):
				total_order_price += prod["price"]
			else:
				for x in range(0,prod["amount"]):
					total_order_price += prod["price"]

		order_number = len(selected_store["orders"]) + 1
		order_object = {
		"orderNum":order_number,
		"totPrice":total_order_price,
		"productsInOrder":input_json["order"]
		}
		selected_store["orders"].append(order_object)
		stores.save(selected_store)

		return jsonify({"order added: ": input_json}), 201
	else:
		return "invalid JSON"

# Adds products to a store via json and POST request
@app.route("/<string:storeName>/add_products", methods=["POST"])
def addProductsViaJSON(storeName):
	stores = mongo.db.Stores
	selected_store = stores.find_one({"name":storeName})
	
	if (request.method == "POST"):
		input_json = request.get_json()
		stores.save(selected_store)
		
		for prod in input_json["products"]:
			selected_store["products"].append(prod)
		
		return jsonify({"products added: ": input_json}), 201
	else:
		return "invalid JSON"
		
# Method allows for the use of new line characters while displaying information
@app.after_request
def treat_as_plain_text(response):
    response.headers["content-type"] = "text/plain"
    return response

if __name__ == "__main__":
	app.run(debug=True)