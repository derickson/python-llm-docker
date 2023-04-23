from langchain import PromptTemplate, LLMChain

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

import sys
sys.path.append('../')
from lib_webLLM import WebLLM


## conversation chains with StableLM 3B
## I don't have the prompt worked out yet.  
## it starts emulating the human back at me rather than continuing the conversation

llm = WebLLM(url="http://davepc:8090/question")

conversation_memory_interaction_length = 3
memory = ConversationBufferWindowMemory( k=conversation_memory_interaction_length )

def main():


    stable_system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
        - StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
        - StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
        - StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
        - StableLM will refuse to participate in anything that could harm a human.
        """
    stable_prompt = f"{stable_system_prompt}"+"<|USER|>{question}<|ASSISTANT|>"
    stable_uninformed_prompt_simple = PromptTemplate(template=stable_prompt, input_variables=["question"])
    stable_uninformed_chain = LLMChain(prompt=stable_uninformed_prompt_simple, llm=llm)


    stable_convo_prompt = """<|SYSTEM|>
        Recent conversation: {history} 
        <|USER|>{input}<|ASSISTANT|>"""

    prompt = PromptTemplate(template=stable_convo_prompt, input_variables=["history","input"])

    conversation = ConversationChain(
            llm=llm, 
            verbose=True, 
            memory=memory,
            prompt=prompt
        )
    conversation.memory.ai_prefix="<|ASSISTANT|>"

    while True:

        question =  input("Ask a question>> ")
        stable_response = conversation.run(input=question)
        print(f"\tAnswer from StableLM : {stable_response}")



if __name__ == '__main__':
    main()



# prior attempts at prompts

    # uninformed_template = """
    # <|SYSTEM|>I am a helpful Assistant that answers questions. When I don't know the answer I say I don't know. 
    # <|USER|>when asked: {question}
    # <|ASSISTANT|>My response is: """
    # uninformed_prompt_simple = PromptTemplate(template=uninformed_template, input_variables=["question"])
    # uninformed_chain = LLMChain(prompt=uninformed_prompt_simple, llm=llm)


    # informed_template = """
    # <|SYSTEM|>I am a helpful Assistant that answers questions using only information in the context.. When I don't know the answer I say I don't know. 
    # <|USER|>I know context: {context}
    # when asked: {question}
    # <|ASSISTANT|>"""
    # informed_prompt_simple = PromptTemplate(template=informed_template, input_variables=["context","question"])
    # informed_chain = LLMChain(prompt=informed_prompt_simple, llm=llm)

    # context = "The president of the United States is Joe Biden."

    # question =  input("Ask a question>> ")
    # uninformed_response = uninformed_chain.run(question=question)
    # print(f"\tAnswer from LLM with no context : {uninformed_response}")

    # print(f"\nLet's try that again with injected context: {context}")
    # informed_response = informed_chain.run(question=question, context=context)
    # print(f"\tAnswer from LLM with context    : {informed_response}")