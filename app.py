from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference, WriteConcern

MONGO_URI = "mongodb+srv://admin:2HguftUYpCAsz0Ns@cluster0.engkol9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000)
db = client["ev_db"]
base_collection = db["vehicles"]

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "EV API running"})

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        coll = base_collection.with_options(
            write_concern=WriteConcern(w=1)
        )
        result = coll.insert_one(data)
        return jsonify({"inserted_id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        coll = base_collection.with_options(
            write_concern=WriteConcern(w="majority")
        )
        result = coll.insert_one(data)
        return jsonify({"inserted_id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    try:
        coll = base_collection.with_options(
            read_preference=ReadPreference.PRIMARY
        )
        count = coll.count_documents({"Make": "TESLA"})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    try:
        coll = base_collection.with_options(
            read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        count = coll.count_documents({"Make": "BMW"})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
