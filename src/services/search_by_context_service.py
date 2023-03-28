from src.repositories.file_indexes_repository import *
from src.clients.openai import openai_client

class SearchByContextService():
    def apply(self, data):
      file_index_repository = FileIndexesRepository()
      
      # get the mongodb entity from the organization
      entity = file_index_repository.get_by_organization(data["organization"])
      
      # send question to open ai and return the answer
      return openai_client.search(data["q"], entity)