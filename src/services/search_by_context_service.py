from src.configs.redis_config import *
import uuid
import json


class SearchByContextService():
    def __init__(self):
        self.redisClient = redis_instance()

    def apply(self, data):
        # generate uuid for the process
        process_uuid = str(uuid.uuid4())

        # add the search request to the queue
        self.redisClient.publish(channel='gpt_search', message=json.dumps({
            'process_uuid': process_uuid,
            'organization': data['organization'],
            'chat_id': data['chat_id'] if 'chat_id' in data else None,
            'q': data['q'],
        }))

        # return the process uuid so the client can check the status
        return process_uuid
