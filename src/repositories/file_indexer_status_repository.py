from pymongo import MongoClient
import os
import datetime

class FileIndexerStatusRepository:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))  
      
        database = os.environ.get('MONGO_INITDB_DATABASE', '')
        collection = 'file_indexer_statuses'
        cursor = self.client[database]
        self.collection = cursor[collection]
    
    def insert(self, data):
        data['created_at'] = datetime.datetime.utcnow()
        response = self.collection.insert_one(data)
        return str(response.inserted_id)
      
    def get_by_process_uuid(self, process_uuid):
      return self.collection.find_one({'process_uuid': process_uuid})