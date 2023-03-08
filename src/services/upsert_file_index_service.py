from src.repositories.file_indexes_repository import *

class UpsertFileIndexService():
    def apply(self, data):
      repository = FileIndexesRepository()
      
      # delete any existing records from organization
      repository.delete({
        "organization": data["organization"]
      })
      
      # add the most recent record (from request) to the organization
      id = repository.insert({
        "Document": data
      })
      
      # returns the record id from mongo
      return str(id)