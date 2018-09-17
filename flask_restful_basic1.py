from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
	def get(self):
		return {"about": "Hello World"}

	def post(self):
		inpJson = request.get_json()
		return {"you sent": inpJson}, 201

class Multi(Resource):
	def get(self, num, num2):
		return {"result": num * num2}

api.add_resource(HelloWorld, "/")
api.add_resource(Multi, "/multi/<int:num>-<int:num2>")

if __name__ == "__main__":
	app.run(debug=True)
