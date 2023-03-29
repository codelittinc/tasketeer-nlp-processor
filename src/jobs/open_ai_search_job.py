from src.clients.openai import openai_client
from src.repositories.file_indexes_repository import *
from src.repositories.open_ai_process_repository import *

class OpenAiSearchJob():
    async def run(self, data, process_uuid):
      # get the mongodb entity from the organization
      entity = FileIndexesRepository().get_by_organization(data["organization"])

      # send question to open ai and wait for the answer
      gpt_result = await openai_client.search(data["q"], entity)
      
      # update the mongodb entity with the answer
      OpenAiProcessRepository().insert({
        'process_uuid': process_uuid,
        'question': data["q"],
        'organization': data['organization'],
        'response': gpt_result.response,
      })
      
      return gpt_result.response