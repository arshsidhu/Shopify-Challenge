Shopify Challenge Winter 2019

Prerequisites:


```
Python 3.6

Flask (Python Framework)

PyMongo (Python Distribution)

```
Installation:

```
Clone the repo and run the python file: "shopify-challenge.py"
```
Database Schema:


Each store follows the schema:
```
{

	name: store_name,

	orders: [list_of_orders]

	products: [list_of_products]

}
```

Each order follows the schema:
```
{

	orderNum: order_number,

	totPrice: total_price_of_order,

	productsInOrder: [list_of_products_in_order]

}
```
Products can follow two different types of schemas


When products are not in an order:
```
{

	name: name_of_product,

	price: price_of_product

}
```
When products are in an order:
```
{

	name: name_of_product,

	price: price_of_product,

	amount: amount_of_product

}
```

API:

Just some notes regarding the API

When sending orders they must follow the schema:
```
{
	order:[list_of_products_in_order]
}
```
Also when sending products in bulk, they must follow the schema:
```
{
	products:[list_of_products]
}
```
For simplicity purposes, I have used MLabs online database service, which allows for a free 500mb service. If more space is needed for testing, you must run a local MongoDB and change the DB_URI value.

There are already two stores in the DB. I have also included a sample json, if my schema was not clear enough

List of Routes:

```
/
	Welcome Page, displays all the stores
/<store-name>
	Dislpays all the products in the store
/<store-name>_orders
	Displays all the orders in the store
/<store-name>_order_numer_<order-number>
	Displays specific order
/delete_<store-name>
	Deletes store
/delete_<store-name>/all_orders
	Deletes all orders in store
/delete_<store-name>/order_number_<order-number>
	Deletes specific order
/delete_<store-name>/product_<product-name>
	Deletes product from store
/delete_<store-name>/order_number_<order-number>/product_<product-name>
	Deletes product from order
/add_store_<store-name>
	Adds new store
/add_<product-name>_<product-price>/<store-name>
	Adds new product to store
/<store-name>/add_to_order/<product-name>
	Starts new order, with product in cart
/<store-name>/add_to_order_number_<order-number>/<product-name>
	Adds product to existing order
```