PROMPT_ANSWER="""
Given the CONTEXT, give a concise answer to the question:
If you don't know the answer, RETURN "I Couldn't find this information in my data." 

CONTEXT: <<PASSAGE>>


QUESTION: <<QUERY>>


CONCISE ANSWER:

"""

PROMPT_SUMMARY="""
Write a friendly concise and detailed summary of the following:

<<SUMMARY>>

FRIENDLY CONCISE AND DETAILED SUMMARY:

"""

LANGCHAIN_TEMPLATE = """
Use the following pieces of "context 1" and "context 2" to answer the question at the end.
Provide a friendly and concise answer to the question.
If you don't know the answer, RETURN "I Couldn't find this information in my data."

CONTEXT 1: {context}

CONTEXT 2: {chat_history}

QUESTION: {question}

CONCISE AND HELPFUL ANSWER:
"""