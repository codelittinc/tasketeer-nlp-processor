from src.jobs.open_ai_search_job import *
import uuid

class SearchByContextService():
    async def apply(self, data):

      # generate uuid for the process
      process_uuid = str(uuid.uuid4())
      
      # run the search job in the background, to not block the main thread
      # asyncio.ensure_future(OpenAiSearchJob().run(data, process_uuid))
      return await OpenAiSearchJob().run(data, process_uuid)