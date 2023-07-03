PROMPT = """
Use the following pieces of "CONTEXT 1" and "CONTEXT 2" to answer the QUESTION at the end.
Provide a friendly and concise answer to the question.
If you don't know the answer, RETURN "I Couldn't find this information in my data."

% START OF CONTEXT 1
"{context}"
% END OF CONTEXT 1

% START OF CONTEXT 2
"{chat_history}"
% END OF CONTEXT 2

% QUESTION: 
- {question}

CONCISE AND HELPFUL ANSWER:
"""