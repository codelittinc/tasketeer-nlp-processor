from src.clients.openai import openai_client
from src.repositories.file_indexes_repository import *
from src.repositories.open_ai_process_repository import *
from src.configs.redis_config import redis_instance
from src.utils.indexing_states import INDEXING_FINISHED, INDEXING_STARTED
import json

class IndexerStartedHandler():
  
    @staticmethod
    def listen():
        redisClient = redis_instance()
        pubsub = redisClient.pubsub()
        pubsub.subscribe('gpt_indexer')
        handler = IndexerStartedHandler()
        for message in pubsub.listen():
            try:
                item = json.loads(message.get('data'))
                handler.run(item['organization'], item['process_uuid'])
            except:
                print("An exception occurred: ", message)
  
  
    def run(self, organization, process_uuid):
      # initialize mongodb repository
      repository = FileIndexesRepository()
      
      # get the initial state of the record (from request) so it can be processed by the indexer
      content = repository.get_by_organization(organization, INDEXING_STARTED)
      
      # generate content index using openai
      indexed_content = openai_client.generate_string_index(content)
      
      # delete any existing records from organization
      repository.delete({
        "organization": organization,
        "state": INDEXING_FINISHED,
      })
      
      # add indexed content to the organization      
      repository.insert({
        "organization": organization,
        "process_uuid": process_uuid,
        "state": INDEXING_FINISHED,
        "content": indexed_content
      })