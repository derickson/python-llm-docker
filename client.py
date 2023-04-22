from langchain import PromptTemplate, LLMChain

from lib_webLLM import WebLLM

llm = WebLLM(url="http://localhost:8080/question")

def main():
    # Your program logic here
    while True:

        template_informed = """
        I am a helpful AI that answers questions. when I don't know the answer I say I don't know. 
        I know: {context}
        when asked: {question}
        my response using only information in the context is: """

        informed_context = "The president of the United States is Joe Biden."

        prompt_informed = PromptTemplate(template=template_informed, input_variables=["context", "question"])
        chain = LLMChain(prompt=prompt_informed, llm=llm)
        

        question =  input("Ask a question>> ")
        informed_response = chain.run(context=informed_context,question=question)
        uninformed_response = llm(question)
        print(f"Answer from LLM with context : {informed_response}")
        print(f"Answer from LLM no context   : {uninformed_response}")

if __name__ == '__main__':
    main()