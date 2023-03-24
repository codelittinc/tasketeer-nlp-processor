from llama_index import (
    GPTTreeIndex,
    LLMPredictor,
    download_loader,
)
import os
from langchain import OpenAI

def _generate_llm_predictor():
  temperature = int(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0'))
  model_name = os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'text-davinci-003')
  
  # define LLM with OpenAI model name and temperature
  return LLMPredictor(llm=OpenAI(temperature=temperature, model_name=model_name))

def generate_string_index(content):
  # download the string loader, in case it doesn't exists
  StringIterableReader = download_loader("StringIterableReader")
  loader = StringIterableReader()
  
  # set the content to be indexed
  documents = loader.load_data(texts=[content])
  
  # define LLM with OpenAI model name and temperature
  llm_predictor = _generate_llm_predictor()

  # index the document 
  index = GPTTreeIndex(documents, llm_predictor=llm_predictor)
  
  # returns the index as a string
  return index.save_to_string()

def search(input, gpt_index_str):
  search_mode = os.environ.get('OPENAI_MODE', 'summarize')
  not_found_answer = os.environ.get('OPENAI_NOT_FOUND_RESPONSE', '')

  if gpt_index_str is None:
    # download the string loader, in case it doesn't exists
    StringIterableReader = download_loader("StringIterableReader")
    loader = StringIterableReader()
    
    # set the content to be indexed
    documents = loader.load_data(texts=['_'])
    
    # define LLM with OpenAI model name and temperature
    llm_predictor = _generate_llm_predictor()
    index = GPTTreeIndex(documents, llm_predictor=llm_predictor)
    return index.query(input, search_mode)
  else:
    index = GPTTreeIndex.load_from_string(gpt_index_str)
    return index.query(f'{input}.{not_found_answer}', search_mode)