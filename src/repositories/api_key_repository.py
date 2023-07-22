from pymongo import MongoClient
import os
from contextlib import contextmanager
from cryptography.fernet import Fernet

class ApiKeyRepository:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_HOST', ''))
        self.fernet_key = os.environ.get('FERNET_KEY', '').encode()
        self.cipher_suite = Fernet(self.fernet_key)
        self.database = os.environ.get('MONGO_INITDB_DATABASE', '')
        self.collection_name = 'api_keys'
        self.fernet_key = Fernet.generate_key()

    @contextmanager
    def get_collection(self):
        db = self.client[self.database]
        collection = db[self.collection_name]
        try:
            yield collection
        finally:
            pass


    def insert(self, organization_id, api_key):
        encrypted_api_key = self.cipher_suite.encrypt(api_key.encode())
        with self.get_collection() as collection:
            response = collection.insert_one({
                'organization_id': str(organization_id),
                'api_key': encrypted_api_key.decode()
            })
        return str(response.inserted_id)

    def get_by_organization_id(self, organization_id):
        with self.get_collection() as collection:
            item = collection.find_one({'organization_id': str(organization_id)})

            if item:
                if 'api_key' in item:
                    decrypted_api_key = self.cipher_suite.decrypt(item['api_key'].encode())
                    item['api_key'] = decrypted_api_key.decode()

            return item
        
    def delete_by_organization_id(self, organization_id):
        with self.get_collection() as collection:
            result = collection.delete_one({'organization_id': str(organization_id)})
            return result.deleted_count

    def encrypt_and_store_key(self, request_data):
        organization_id = request_data['organization_id']
        api_key = request_data['api_key']
        encrypted_api_key = self.cipher_suite.encrypt(api_key.encode())

        with self.get_collection() as collection:   
            existing_key = collection.find_one({'organization_id': str(organization_id)})
            if existing_key:
                collection.update_one({'_id': existing_key['_id']}, {'$set': {'api_key': encrypted_api_key.decode()}})
                return {'status': 'API key updated successfully'}
            else:
                collection.insert_one({
                    'organization_id': str(organization_id),
                    'api_key': encrypted_api_key.decode()
                })
                return {'status': 'API key stored successfully'}
