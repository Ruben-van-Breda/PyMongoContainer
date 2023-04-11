import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydb" # Note that "mongo" is the name of the MongoDB container

client = MongoClient('mongo', 27017)
db = client['mydb']
collection = db['users']
PORT = int(os.environ.get("PORT", 3000))



@app.route("/")
def home():
    return "<h1>Hello World!</h1>"

@app.route("/add", methods=["POST"])
def add_data():
    # get request arguments
    name = request.args.get("name")
    age = request.args.get("age")

    print("data_to_add: ", name)
    data = {}
    data['name'] = name
    data['age'] = age

    collection.users.insert_one(data)
    return redirect('/view')

@app.route("/view")
def view():
    users = collection.users.find()
    output = []
    for user in users:
        output.append({"name": user["name"], "age": user["age"]})
    return jsonify({"users": output})







def DropTable():
    collection.users.drop()






if __name__ == "__main__":
    print("Starting app on port {}".format(PORT))
    app.run(debug=True, host="0.0.0.0", port=PORT)
