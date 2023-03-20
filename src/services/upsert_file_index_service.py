from src.repositories.file_indexes_repository import *
from src.clients.openai import openai_client

class UpsertFileIndexService():
    def apply(self, data):
      # validate required params
      self._validate(data)
      
      # initialize mongodb repository
      repository = FileIndexesRepository()
      
      # check if there is any file already indexed for organization
      file_index = repository.get_by_organization(data["organization"]) 
      
      # generate content index using openai
      data["content"] = openai_client.generate_string_index(data["content"], file_index)
      
      # delete any existing records from organization
      repository.delete({
        "organization": data["organization"]
      })
      
      # add the most recent record (from request) to the organization
      response = repository.insert({
        "Document": data
      })
      
      # returns the record id from mongo
      return response
    
    def _validate(self, data):      
      if not data["organization"]:
        raise Exception("Organization is required")
      if not data["content"]:
        raise Exception("Content is required")