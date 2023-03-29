from llama_index import (
    GPTSimpleVectorIndex,
    LLMPredictor,
    StringIterableReader,
    ServiceContext,
)
import os
import openai
from langchain.chat_models import ChatOpenAI

def generate_string_index(content):
  temperature = int(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0'))
  model_name = os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'gpt-3.5-turbo')

  # set the string loader to be used by the index
  loader = StringIterableReader()
  
  # set the content to be indexed
  documents = loader.load_data(texts=[content])
  
  # define LLM with OpenAI model name and temperature
  llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=temperature, model_name=model_name, max_tokens=512))

  # index the document 
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
  index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
  
  # returns the index as a string
  return index.save_to_string()

async def search(input, gpt_index_str):
  not_found_answer = os.environ.get('OPENAI_NOT_FOUND_RESPONSE', '')

  # in case there are no indexed documents, use the default openai completion api
  # otherwise, use the indexed documents to search for the answer
  # PS: Completion API does not support the gpt-3.5-turbo model at the time of this writing 
  if gpt_index_str is None:
    completion = openai.Completion.create(model="text-davinci-003", prompt=f'{input}.{not_found_answer}')
    return { 'response': completion.choices[0].text }
  else:
    index = GPTSimpleVectorIndex.load_from_string(gpt_index_str)
    return index.query(f'{input}.{not_found_answer}')