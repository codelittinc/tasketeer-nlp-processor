import os
import openai
import pinecone
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from src.clients.openai.openai_prompt_messages import LANGCHAIN_TEMPLATE
from src.clients.openai.loaders.nlp_google_drive_loader import NlpGoogleDriveLoader


def generate_string_index(content, organization, google_drive_id, google_token, openai_api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    # Load from provided content
    documents = [Document(page_content=content)]
    google_drive_documents = __google_drive_loader(google_drive_id, google_token)
        
    # Split documents into smaller chunks
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    google_drive_chunks = text_splitter.split_documents(google_drive_documents)

    # Generate embeddings and index
    __init_pinecone()
    Pinecone.from_texts(
        [t.page_content for t in docs], embeddings,
        index_name=os.environ.get('PINECONE_INDEX'),
        namespace=f"organization-{organization}"
    )
    
    # Generate embeddings and index for google drive documents
    if len(google_drive_chunks) > 0:
        Pinecone.from_texts(
            [t.page_content for t in google_drive_chunks], embeddings,
            index_name=os.environ.get('PINECONE_INDEX'),
            namespace=f"org-google-drive-{organization}"
        )
    return True


def search(req_input, organization, openai_api_key, history=None):
    __init_pinecone()
    openai.api_key = openai_api_key
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    chain = Pinecone.from_existing_index(
        os.environ.get('PINECONE_INDEX'), embeddings,
        namespace=f"organization-{organization}"
    )
    google_drive_chain = Pinecone.from_existing_index(
        os.environ.get('PINECONE_INDEX'), embeddings,
        namespace=f"org-google-drive-{organization}"
    )    
    
    similar_docs = chain.similarity_search(req_input)
    similar_docs.extend(google_drive_chain.similarity_search(req_input))

    prompt = PromptTemplate(template=LANGCHAIN_TEMPLATE, input_variables=["context", "question", "chat_history"])

    llm = ChatOpenAI(
        model_name=os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'gpt-3.5-turbo-16k'),
        temperature=float(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0')),
        max_tokens=int(os.environ.get('OPENAI_PREDICTOR_TOKENS', '3000')),
    )

    if history is None:
        history = [
            { 'question': '', 'response': '' },
        ]
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question", 
    )
    for message in reversed(history):
        memory.chat_memory.add_user_message(message['question'])
        memory.chat_memory.add_ai_message(message['response'])

    chain = load_qa_chain(
        llm, 
        chain_type="stuff", 
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    answer = chain.run(input_documents=similar_docs, question=req_input, chat_history=memory.chat_memory)
    return answer

def __init_pinecone():
    pinecone.init(
        api_key=os.environ.get('PINECONE_API_KEY', ''),  # find at app.pinecone.io
        environment=os.environ.get('PINECONE_ENV', '')  # next to api key in console
    )

def __google_drive_loader(google_drive_id, google_token):
    if google_drive_id is None or google_token is None:
        return []

    loader = NlpGoogleDriveLoader(
        folder_id=google_drive_id,
        google_token=google_token,
        recursive=True,
        verbose=True
    )
    docs = loader.load()
    return docs;