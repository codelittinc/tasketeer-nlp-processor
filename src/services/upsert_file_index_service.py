from src.repositories.file_indexes_repository import *
from src.configs.redis_config import *
from src.utils.indexing_states import INDEXING_STARTED
import uuid
import json

class UpsertFileIndexService():
    def __init__(self):
      self.redisClient = redis_instance()
    
    def apply(self, data):
      
      # validate required params
      self._validate(data)
      
      repository = FileIndexesRepository()
      
      # generate uuid for the process
      process_uuid = str(uuid.uuid4())
      
      # delete any existing records from organization
      repository.delete({
        "organization": data["organization"],
        "state": INDEXING_STARTED,
      })
      
      # add the initial state of the record (from request) so it can be processed by the indexer
      repository.insert({
        "organization": data["organization"],
        "process_uuid": process_uuid,
        "state": INDEXING_STARTED,
        "content": data["content"]
      })

      # add the search request to the queue
      self.redisClient.publish(channel='gpt_indexer', message=json.dumps({
        'process_uuid': process_uuid,
        'organization': data['organization'],
        'google_drive_id': data['google_drive_id'] if 'google_drive_id' in data else None,
        'google_token': data['google_token']  if 'google_token' in data else None,
      }))

      # return the process uuid so the client can check the status
      return {'status': 'Successfully Inserted', 'document_id': process_uuid }
    
    def _validate(self, data):      
      if not data["organization"]:
        raise Exception("Organization is required")
      if not data["content"] and not data["google_drive_id"]:
        raise Exception("Content is required")