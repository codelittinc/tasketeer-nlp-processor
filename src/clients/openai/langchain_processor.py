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

embeddings = OpenAIEmbeddings()
openai.api_key = os.environ.get('OPENAI_API_KEY', '')


def init_pinecone():
    pinecone.init(
        api_key=os.environ.get('PINECONE_API_KEY', ''),  # find at app.pinecone.io
        environment=os.environ.get('PINECONE_ENV', '')  # next to api key in console
    )


def generate_string_index(content, organization):
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents([Document(page_content=content)])

    init_pinecone()
    Pinecone.from_texts(
        [t.page_content for t in docs], embeddings,
        index_name=os.environ.get('PINECONE_INDEX'),
        namespace=f"organization-{organization}"
    )
    return True


def search(req_input, organization):
    init_pinecone()
    openai.api_key = os.environ.get('OPENAI_API_KEY', '')
    chain = Pinecone.from_existing_index(
        os.environ.get('PINECONE_INDEX'), embeddings,
        namespace=f"organization-{organization}"
    )
    similar_docs = chain.similarity_search(req_input)

    template = """
    Use the following pieces of context to answer the question at the end.
    Provide a friendly and concise answer to the question.
    If you don't know the answer, RETURN "I Couldn't find this information in my data.", don't try to make up an answer.
    
    CONTEXT: {context}

    QUESTION: {question}
   
    CONCISE AND HELPFUL ANSWER:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = ChatOpenAI(
        model_name=os.environ.get('OPENAI_PREDICTOR_MODEL_NAME', 'gpt-3.5-turbo'),
        temperature=float(os.environ.get('OPENAI_PREDICTOR_TEMPERATURE', '0')),
        max_tokens=int(os.environ.get('OPENAI_PREDICTOR_TOKENS', '3000')),
    )
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    answer = chain.run(input_documents=similar_docs, question=req_input)
    return answer
