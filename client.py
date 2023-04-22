from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

import requests

url = "http://localhost:8000/question"

class CustomLLM(LLM):
    
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        payload = {
            "question": prompt
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(response.json())
            return str(response.json()["answer"][0])
        else:
            return "error don't know"
        
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"notsure": "notsure"}
    
llm = CustomLLM()



def main():
    # Your program logic here
    while True:
        question =  input("Ask a question>> ")
        response = llm(question)
        print(f"Answer from LLM: {response}")


if __name__ == '__main__':
    main()