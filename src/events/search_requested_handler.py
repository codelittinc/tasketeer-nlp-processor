from src.clients.openai import openai_client
from src.repositories.file_indexes_repository import *
from src.repositories.open_ai_process_repository import *
from src.configs.redis_config import redis_instance
import json

class SearchRequestedHandler():
  
    @staticmethod
    def listen():
        redisClient = redis_instance()
        pubsub = redisClient.pubsub()
        pubsub.subscribe('gpt_search')
        handler = SearchRequestedHandler()
        for message in pubsub.listen():
            try:
                item = json.loads(message.get('data'))
                handler.run(item, item['process_uuid'])
            except:
                print("An exception occurred: ", message)
  
  
    def run(self, data, process_uuid):
      # get the mongodb entity from the organization
      entity = FileIndexesRepository().get_by_organization(data["organization"])

      # send question to open ai and wait for the answer
      gpt_result = openai_client.search(data["q"], entity)
      
      # update the mongodb entity with the answer
      OpenAiProcessRepository().insert({
        'process_uuid': process_uuid,
        'question': data["q"],
        'organization': data['organization'],
        'response': gpt_result.response,
      })
      
      return gpt_result.response