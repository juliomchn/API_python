from pymongo import MongoClient

# Run DataBase in local
#"D:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="D:\Users\50051512\Julio\MongoDB"

#db_connection = MongoClient().local

db_connection = MongoClient("mongodb+srv://test:test@cluster0.atr9von.mongodb.net/?retryWrites=true&w=majority").test