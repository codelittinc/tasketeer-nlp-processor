from llama_index import (
    GPTTreeIndex, 
    LLMPredictor,
    download_loader,
)
import os
from langchain import OpenAI

def generate_string_index(content):
  temperature = int(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0'))
  model_name = os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'text-davinci-003')
  
  # download the string loader, in case it doesn't exists
  StringIterableReader = download_loader("StringIterableReader")
  loader = StringIterableReader()
  
  # set the content to be indexed
  documents = loader.load_data(texts=[content])

  # define LLM
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=temperature, model_name=model_name))

  # build index
  index = GPTTreeIndex(documents, llm_predictor=llm_predictor)

  return index.save_to_string()


def search(input, gpt_index_str):
  search_mode = os.environ.get('OPENAI_MODE', 'summarize')
  not_found_answer = os.environ.get('OPENAI_NOT_FOUND_RESPONSE', '')

  # build index
  index = GPTTreeIndex.load_from_string(gpt_index_str)
  return index.query(f'{input}.{not_found_answer}', search_mode)