from llama_index import (
    GPTTreeIndex, 
    LLMPredictor,
    download_loader,
)
import os

from langchain import OpenAI

def generate_string_index(content):
  temperature = int(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0'))
  model_name = os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', '')
  
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