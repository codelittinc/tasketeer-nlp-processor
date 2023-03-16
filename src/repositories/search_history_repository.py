from pymongo import MongoClient
import os
import datetime

class SearchHistoryRepository:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))  
      
        database = os.environ.get('MONGO_INITDB_DATABASE', '')
        collection = 'search_history'
        cursor = self.client[database]
        self.collection = cursor[collection]
    
    def insert(self, data):
        data['created_at'] = datetime.datetime.utcnow()
        response = self.collection.insert_one(data)
        output = {'status': 'Successfully Inserted',
                  'document_id': str(response.inserted_id)}
        return output