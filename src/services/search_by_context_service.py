from src.jobs.open_ai_search_job import *
import uuid

class SearchByContextService():
    async def apply(self, data):

      # generate uuid for the process
      process_uuid = str(uuid.uuid4())
      
      # run the job
      await OpenAiSearchJob().run(data, process_uuid)
      
      # return the process uuid so the client can check the status
      return process_uuid