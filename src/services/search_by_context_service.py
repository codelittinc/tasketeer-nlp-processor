from src.repositories.file_indexes_repository import *
from src.repositories.search_history_repository import *
from src.clients.openai import openai_client

class SearchByContextService():
    def apply(self, data):
      file_index_repository = FileIndexesRepository()
      search_history_repository = SearchHistoryRepository()
      
      # get the mongodb entity from the organization
      entity = file_index_repository.get_by_organization(data["organization"])
      
      # send question to open ai
      response = openai_client.search(data["q"], entity['content'])
      
      # add response to the search history collection
      search_history_repository.insert({
        'organization': data["organization"],
        'q': data["q"],
        'gpt_answer': str(response),
        'gpt_file_index': entity
      })
      
      # returns the anwser from open ai
      return response