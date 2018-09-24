Shopify Challenge Winter 2019

Prerequisites:
Python 3.6
Flask (Python Framework)
PyMongo (Python Distribution)

Installation:
Clone the repo and run the python file: "shopify-challenge.py"

Database Schema:
Each store follows the schema:
{
	name: store_name,
	orders: [list_of_orders]
	products: [list_of_products]
}

Each order follows the schema:
{
	orderNum: order_number,
	totPrice: total_price_of_order,
	productsInOrder: [list_of_products_in_order]
}

Products can follow two different types of schemas

When products are not in an order:
{
	name: name_of_product,
	price: price_of_product
}

When products are in an order:
{
	name: name_of_product,
	price: price_of_product,
	amount: amount_of_product
}

For simplicity purposes, I have used MLabs online database service, which allows for a free 500mb service. If more space is needed for testing, you must run a local MongoDB and change the DB_URI value.