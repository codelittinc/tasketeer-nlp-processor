import os
import openai
import json
import textwrap
import asyncio
from src.clients.openai.openai_prompt_messages import PROMPT_ANSWER, PROMPT_SUMMARY
from src.clients.openai.openai_utils import gpt3_embedding, search_index, gpt3_completion

def generate_string_index(content):
  openai.api_key = os.environ.get('OPENAI_API_KEY', '')
  chunck_size = int(os.environ.get('OPENAI_INDEXER_CHUNK_SIZE', '3000'))

  chunks = textwrap.wrap(content, chunck_size)
  result = list()
  for index, chunk in enumerate(chunks):
    print('Indexing chunk ' + str(index) + ' of ' + str(len(chunks)))
    embedding = gpt3_embedding(chunk.encode(encoding='ASCII',errors='ignore').decode())
    info = {'content': chunk, 'vector': embedding}
    result.append(info)
  
  # returns the index as a string
  print("Indexing completed. Returning index as string.")
  return json.dumps(result)

async def search(input, gpt_index_str):
  openai.api_key = os.environ.get('OPENAI_API_KEY', '')

  data = json.loads(gpt_index_str)
  results = search_index(input, data)
  answers = list()
  tasks = []
  
  # answer the same question for all returned chunks that are similar to the input
  for result in results:
    prompt = PROMPT_ANSWER.replace('<<PASSAGE>>', result['content']).replace('<<QUERY>>', input)
    
    # adds the task to the list of tasks to be executed in open ai
    tasks.append(asyncio.create_task(gpt3_completion(prompt)))
      
  # wait for all tasks to complete
  answers = await asyncio.gather(*tasks)
  
  # do not consider anwsers that are not found in the data
  answers = [answer for answer in answers if answer != "I couldn't find this information in my data."]
        
  # summarize the answers together
  all_answers = '\n\n'.join(answers)
  chunks = textwrap.wrap(all_answers, 10000)
  final = list()
  for chunk in chunks:
    prompt = PROMPT_SUMMARY.replace('<<SUMMARY>>', chunk)
    summary = await gpt3_completion(prompt)
    final.append(summary)
  return '\n\n'.join(final)