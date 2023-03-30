from pymongo import MongoClient
import os
import gridfs

class FileIndexesRepository:
    def __init__(self):
        database = os.environ.get('MONGO_INITDB_DATABASE', '')
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))
        cursor = self.client[database]
        self.fs = gridfs.GridFS(cursor)  
    
    def get_by_organization(self, organization):
        item = self.fs.find_one({'organization': organization})
        return item.read().decode('utf-8') if item else None
    
    def insert(self, data):
        organization = data["organization"]
        process_uuid = data["process_uuid"]
        state = data["state"]
        content = data["content"]
        
        id = self.fs.put(content, organization=organization, process_uuid=process_uuid, state=state, encoding='utf-8')
        return {'status': 'Successfully Inserted', 'document_id': str(id)}
    
    def delete(self, data):
        item = self.fs.find_one({'organization': data['organization']})
        if item is None:
            return {'status': 'Document not found.'}
        return self.fs.delete(item._id)