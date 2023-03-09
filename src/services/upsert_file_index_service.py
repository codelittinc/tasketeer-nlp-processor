from src.repositories.file_indexes_repository import *
from src.clients.openai import openai_client

class UpsertFileIndexService():
    def apply(self, data):
      repository = FileIndexesRepository()
      
      # delete any existing records from organization
      repository.delete({
        "organization": data["organization"]
      })
      
      # generate content index using openai
      data["content"] = openai_client.generate_string_index(data["content"])
      
      # add the most recent record (from request) to the organization
      id = repository.insert({
        "Document": data
      })
      
      # returns the record id from mongo
      return str(id)