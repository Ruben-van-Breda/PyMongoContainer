import json
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from markupsafe import escape
from bson import json_util

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
    data = {}
    id = collection.users.count_documents({}) + 1

    for arg in request.args:
        data[arg] = request.args.get(arg)
        data['id'] = id    
    
    collection.users.insert_one(data)
    return redirect('/view')

@app.route("/view")
def view():
    users = collection.users.find()
    output = []
    for user in users:
        print(user)
        # Convert the query result to a JSON string
        json_str = json_util.dumps(user)
        # Convert the JSON string to a Python dictionary
        json_obj = json.loads(json_str)
        # drop field
        json_obj.pop('_id')
        output.append(json_obj)
    
    return jsonify({"users": output}), 200



@app.route("/view/<int:id>")
def view_one(id : int):
    id = int(id)
    try:
        user = collection.users.find_one({"id": id})
        json_obj = json.loads(json_util.dumps(user))
        json_obj.pop('_id')
        # user_json = {"id": user["id"], "name": user["name"], "age": user["age"]}
        return jsonify(json_obj), 200
    except Exception as e:
        return jsonify({"error": "User not found. " + str(e) }), 404

@app.route("/view/")
def view_item():
    # get request argument and argment value
    query_params = request.args

    # if no argument is passed, return all users
    if not query_params:
        return redirect('/view')
    
    # if argument is passed, return user with that argument
    json_query = {}
    for arg in query_params:        
        json_query[arg] = query_params.get(arg)

    try:
        users = []
        for user in collection.users.find(json_query):
            json_obj = json.loads(json_util.dumps(user))
            json_obj.pop('_id')
            users.append(json_obj)
            # user_json = {"id": user["id"], "name": user["name"], "age": user["age"]}
        
        return jsonify(users), 200
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
