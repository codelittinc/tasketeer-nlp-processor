from src.repositories.file_indexes_repository import *
from src.configs.redis_config import *
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
        "organization": data["organization"]
      })
      
      # add the initial state of the record (from request) so it can be processed by the indexer
      repository.insert({
        "organization": data["organization"],
        "process_uuid": process_uuid,
        "state": "started",
        "content": data["content"]
      })
      
      # add the search request to the queue
      self.redisClient.publish(channel='gpt_indexer', message=json.dumps({
        'process_uuid': process_uuid,
        'organization': data['organization']
      }))
      
      # return the process uuid so the client can check the status
      return {'status': 'Successfully Inserted', 'document_id': process_uuid }
    
    def _validate(self, data):      
      if not data["organization"]:
        raise Exception("Organization is required")
      if not data["content"]:
        raise Exception("Content is required")