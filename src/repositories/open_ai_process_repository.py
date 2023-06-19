from pymongo import MongoClient
import os
import datetime

class OpenAiProcessRepository:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))  
      
        database = os.environ.get('MONGO_INITDB_DATABASE', '')
        collection = 'open_ai_processes'
        cursor = self.client[database]
        self.collection = cursor[collection]
    
    def insert(self, data):
        data['processed_at'] = datetime.datetime.utcnow()
        response = self.collection.insert_one(data)
        return str(response.inserted_id)

    def get_by_process_uuid(self, process_uuid):
        return self.collection.find_one({'process_uuid': process_uuid})

    def get_chat_history(self, chat_id, limit):
        history = self.collection.find({
            'chat_id': chat_id,
            'response': {
                '$not': {
                    '$regex': r'^I Couldn\'t find this information in my data\.$',
                    '$options': 'i'
                }
            }
        }, {
            'question': 1, 
            'response': 1,
            'created_at': 1,
        }).sort('created_at', -1).limit(limit)
        return list(history)