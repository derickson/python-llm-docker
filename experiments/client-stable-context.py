from langchain import PromptTemplate, LLMChain

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

import sys
sys.path.append('../')
from lib_webLLM import WebLLM

VERBOSE = False


## This is a test calling StableLM 3B hosted on a local Windows PC behind a REST service
## what I've learned is that I can get it to use information from context, but it won't ignore what's in the pretrained model

## 

llm = WebLLM(url="http://davepc:8090/question")

uninformed_template = """
<|SYSTEM|>I am a helpful Assistant that answers questions. When I don't know the answer I say I don't know. 
<|USER|>when asked: {question}
<|ASSISTANT|>My response is: """
uninformed_prompt_simple = PromptTemplate(template=uninformed_template, input_variables=["question"])
uninformed_chain = LLMChain(prompt=uninformed_prompt_simple, llm=llm)


informed_template = """
<|SYSTEM|>I answer questions using information in the context. When I don't know the answer or the information isn't from the context I say "I don't know". 
The context: {context}
<|USER|>{question}
<|ASSISTANT|>"""
informed_prompt_simple = PromptTemplate(template=informed_template, input_variables=["context","question"])
informed_chain = LLMChain(prompt=informed_prompt_simple, llm=llm)

context = "WHODATHUNKITYO is a cat and is the current president of Cat Land."

def main():

    while True:
        print("")
        question =  input("Ask a question>> ")
        # uninformed_response = uninformed_chain.run(question=question)
        # if VERBOSE:
        #     print(f"\tAnswer from LLM with no context : {uninformed_response}")
        # else:
        #     print(f"\t{uninformed_response}")

        if VERBOSE: print(f"\nLet's try that again with injected context: {context}")
        informed_response = informed_chain.run(question=question, context=context)
        if VERBOSE: 
            print(f"\tAnswer from LLM with context    : {informed_response}")
        else:
            print(f"\t{informed_response}")

if __name__ == '__main__':
    main()



