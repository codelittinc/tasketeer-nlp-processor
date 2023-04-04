PROMPT_ANSWER="""
Use my data to give a concise answer to the question:
If you don't know the answer, RETURN "I Couldn't find this information in my data." 

QUESTION: <<QUERY>>


MY DATA: <<PASSAGE>>


CONCISE ANSWER:

"""

PROMPT_SUMMARY="""
Write an informal and creative detailed summary of the following:

<<SUMMARY>>

INFORMAL AND CREATIVE DETAILED SUMMARY:

"""