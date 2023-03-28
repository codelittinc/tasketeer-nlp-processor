from llama_index import (
    GPTTreeIndex,
    LLMPredictor,
    download_loader,
)
import os
import openai
from langchain import OpenAI

def generate_string_index(content):
  temperature = int(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0'))
  model_name = os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'gpt-3.5-turbo')

  # download the string loader, in case it doesn't exists
  StringIterableReader = download_loader("StringIterableReader")
  loader = StringIterableReader()
  
  # set the content to be indexed
  documents = loader.load_data(texts=[content])
  
  # define LLM with OpenAI model name and temperature
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=temperature, model_name=model_name))

  # index the document 
  index = GPTTreeIndex(documents, llm_predictor=llm_predictor)
  
  # returns the index as a string
  return index.save_to_string()

def search(input, gpt_index_str):
  search_mode = os.environ.get('OPENAI_MODE', 'summarize')
  not_found_answer = os.environ.get('OPENAI_NOT_FOUND_RESPONSE', '')

  # in case there are no indexed documents, use the default openai completion api
  # otherwise, use the indexed documents to search for the answer
  # PS: Completion API does not support the gpt-3.5-turbo model at the time of this writing 
  if gpt_index_str is None:
    completion = openai.Completion.create(model="text-davinci-003", prompt=f'{input}.{not_found_answer}')
    return { 'response': completion.choices[0].text }
  else:
    index = GPTTreeIndex.load_from_string(gpt_index_str)
    return index.query(f'{input}.{not_found_answer}', search_mode)