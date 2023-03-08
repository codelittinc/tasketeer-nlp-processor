from pymongo import MongoClient
import os
import datetime
import sys

class FileIndexesRepository:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))  
      
        database = os.environ.get('MONGO_INITDB_DATABASE', '')
        collection = 'file_indexes'
        cursor = self.client[database]
        self.collection = cursor[collection]
    
    
    def insert(self, data):
        new_document = data['Document']
        new_document['created_at'] = datetime.datetime.utcnow()
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output
    
    def delete(self, data):
        response = self.collection.delete_one({'organization': data['organization']})
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output