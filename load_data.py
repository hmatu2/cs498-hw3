import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://admin:2HguftUYpCAsz0Ns@cluster0.engkol9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000)
db = client["ev_db"]
collection = db["vehicles"]

df = pd.read_csv("Electric_Vehicle_Population_Data.csv")
records = df.to_dict(orient="records")

collection.delete_many({})

batch_size = 1000
for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    collection.insert_many(batch)
    print(f"Inserted {i + len(batch)} / {len(records)}")

print("Data uploaded!")
print("Total documents:", collection.count_documents({}))







