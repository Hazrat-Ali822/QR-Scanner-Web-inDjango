client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]