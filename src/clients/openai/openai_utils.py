import openai
import os
import re
from time import sleep
from openai.datalib import numpy as np

# define a function to calculate the cosine similarity between two vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# define a function to search the index for the most similar vector
def search_index(text, data):
  
  # get the number of most similar results to consider during searches
  count=int(os.environ.get('OPENAI_INDEXER_SEARCH_COUNT', '20'))
  
  # calculate the vector for the input text
  vector = gpt3_embedding(text)
  
  scores = list()
  for i in data:
    score = cosine_similarity(vector, i['vector'])
    scores.append({'content': i['content'], 'score': score})
  ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
  
  # return the top X most similar results
  return ordered[0:count]

# define a function to calculate the vector for a given text
def gpt3_embedding(content):
  engine = os.environ.get('OPENAI_EMBEDDING_MODEL_NAME', 'text-embedding-ada-002')
  
  # create the embedding in openai for the text
  response = openai.Embedding.create(input=content,engine=engine)
  vector = response['data'][0]['embedding']
  return vector

async def gpt3_completion(prompt, stop=['<<END>>']):
  
  # in case the open ai request fail, set 5 other retries
  max_retry = 5
  retry = 0
  prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
  while True:
    try:
      response = openai.ChatCompletion.create(
        model=os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'gpt-3.5-turbo'),
        messages=[
            {"role": "system", "content": os.environ.get('OPENAI_PREDICTOR_ASSISTANT_PERSONA', '')},
            {'role': 'user', 'content': prompt}
        ],
        temperature=float(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0')),
        max_tokens=float(os.environ.get('OPENAI_PREDICTOR_TOKENS', '3000')),
        top_p=float(os.environ.get('OPENAI_PREDICTOR_TOP_P', '1.0')),
        frequency_penalty=float(os.environ.get('OPENAI_PREDICTOR_FREQUENCY_PENALTY', '0.25')),
        stop=stop)
      text = response['choices'][0]['message']['content'].strip()
      if text.lower() == "i couldn't find this information in my data.":
        return None
      
      text = re.sub('\s+', ' ', text)
      return text
    except Exception as oops:
      retry += 1
      if retry >= max_retry:
          raise Exception("Error communicating with OpenAI after " + str(max_retry) + " retries. ", oops)
      print('Error communicating with OpenAI:', oops)
      sleep(1)