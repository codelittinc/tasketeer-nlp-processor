from src.clients.openai import openai_client
from src.repositories.file_indexes_repository import *
from src.repositories.open_ai_process_repository import *
from src.configs.redis_config import redis_instance
from src.utils.indexing_states import INDEXING_FINISHED
import json
import asyncio

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
                asyncio.run(handler.run(item, item['process_uuid']))
            except Exception as e:
                print("An exception occurred, payload: ", message)
                print(e)
  
  
    async def run(self, data, process_uuid):
      # get the mongodb entity from the organization
      entity = FileIndexesRepository().get_by_organization(data["organization"], INDEXING_FINISHED)

      # send question to open ai and wait for the answer
      gpt_result = await openai_client.search(data["q"], entity)
      
      # update the mongodb entity with the answer
      OpenAiProcessRepository().insert({
        'process_uuid': process_uuid,
        'question': data["q"],
        'organization': data['organization'],
        'response': gpt_result,
      })
      
      return gpt_result