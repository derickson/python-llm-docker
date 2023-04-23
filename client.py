from langchain import PromptTemplate, LLMChain
from lib_webLLM import WebLLM


## Connects to a hosted instance of T5 Flan sitting behind a rest service
## Is able to answer questions from context
## It isn't doing a good job of saying I don't know.

llm = WebLLM(url="http://nuc:8090/question")

def main():
    while True:

        template_informed = """
        I am a helpful AI that answers questions. When I don't know the answer I say I don't know. 
        I know context: {context}
        when asked: {question}
        my response using only information in the context is: """

        informed_context = "NOTAREALCAT is a cat and is the current president of Cat Land."
        # informed_context = "The president of the United States is Joe Biden."

        prompt_informed = PromptTemplate(template=template_informed, input_variables=["context", "question"])
        chain = LLMChain(prompt=prompt_informed, llm=llm)
        

        question =  input("Ask a question>> ")
        print(f"Injected Context: {informed_context}")
        informed_response = chain.run(context=informed_context,question=question)
        uninformed_response = llm(question)
        print(f"\tAnswer from LLM with context         : {informed_response}")
        print(f"\tAnswer from LLM no context or prompt : {uninformed_response}")

if __name__ == '__main__':
    main()