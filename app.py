import json
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from markupsafe import escape


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydb" # Note that "mongo" is the name of the MongoDB container

client = MongoClient('mongo', 27017)
db = client['mydb']
collection = db['users']
PORT = int(os.environ.get("PORT", 3000))



@app.route("/")
def home():
    DropTable()
    return "<h1>Hello World!</h1>"

@app.route("/add", methods=["POST"])
def add_data():
    # get request arguments
    name = request.args.get("name")
    age = request.args.get("age")
    # add unique id to data
    id = collection.users.count_documents({}) + 1

    print("data_to_add: ", name)
    data = {}
    data['id'] = id
    data['name'] = name
    data['age'] = age

    collection.users.insert_one(data)
    return redirect('/view')

@app.route("/view")
def view():
    print("Viewing users.")
    users = collection.users.find()
    output = []
    for user in users:
        print(user)
        output.append({"id": user["id"], "name": user["name"], "age": user["age"]})
    return jsonify({"users": output})



@app.route("/view/<int:id>")
def view_one(id : int):
    id = int(id)
    try:
        user = collection.users.find_one({"id": id})
        user_json = {"id": user["id"], "name": user["name"], "age": user["age"]}
        return jsonify(user_json), 200
    except Exception as e:
        return jsonify({"error": "User not found. " + str(e) }), 404


@app.route("/view/<int:id>/<arg>")
def view_items_arg(id, arg : str):
    id = int(id)
    try:
        user = collection.users.find_one({"id": id})
        user_json = {str(arg): user[arg]}
        return jsonify(user_json), 200
    except Exception as e:
        return jsonify({"error": f"User not found or invalid argument {arg}" + str(e) }), 404


@app.route("/delete/<int:id>")
def delete(id : int):
    # convert variable paramater to int
    id = int(id)
    print("Deleting user.")

    # name : str = escape(id)
    # print(f"Searching for user: {name}")
    try:
        collection.users.delete_one({"id": id})
        return redirect('/view')
    except Exception as e:
        return jsonify({"error": "User not found. " + str(e) })
    
    





def DropTable():
    collection.users.drop()






if __name__ == "__main__":
    print("Starting app on port {}".format(PORT))
    app.run(debug=True, host="0.0.0.0", port=PORT)
