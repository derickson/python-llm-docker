## for conversation LLM
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from langchain.llms import HuggingFacePipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM, StoppingCriteria, StoppingCriteriaList
import gc
import os



OPTION_CUDA_USE_GPU = os.getenv('OPTION_CUDA_USE_GPU', 'False') == "True"
cache_dir="./cache"


def clean_cache(p=False):
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    if p:
        print(f"TORCH CUDA MEMORY ALLOCATED: {torch.cuda.memory_allocated()/(1024)} Kb")

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [50278, 50279, 50277, 1, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


def getStableLM3B():
    model_id = 'stabilityai/stablelm-tuned-alpha-3b'
    print(f">> Prep. Get {model_id} ready to go")
    tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir) 
    clean_cache()
    model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=cache_dir)
    clean_cache()
    pipe = pipeline(
        "text-generation",
        model=model, 
        tokenizer=tokenizer, 
        max_length=256,
        temperature=0.7,
        stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
        pad_token_id=50256, num_return_sequences=1
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm



def getFlanXL():
    
    model_id = 'google/flan-t5-large'
    print(f">> Prep. Get {model_id} ready to go")
    # model_id = 'google/flan-t5-large'# go for a smaller model if you dont have the VRAM
    tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir) 
    if OPTION_CUDA_USE_GPU:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_id,cache_dir=cache_dir, load_in_8bit=True, device_map='auto') 
            model.cuda()
    else:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id,cache_dir=cache_dir) 
    
    pipe = pipeline(
        "text2text-generation",
        model=model, 
        tokenizer=tokenizer, 
        max_length=100
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

## options are flan and stablelm
MODEL = "flan"


if MODEL == "flan":
    local_llm = getFlanXL()
else:
    local_llm = getStableLM3B()

def get_llm():
    return local_llm


# def make_the_llm():
#     if MODEL == "flan":
#         template_informed = """
#         I know: {context}
#         when asked: {question}
#         my response is: """
#     else:
#         stablelm_system_prompt = """
#             - StableLM answers questions using only the information {context}
#             - If it does not have the information, StableLM answers with 'I do not know'
#         """
#         template_informed  = f"<|SYSTEM|>{stablelm_system_prompt}"+"<|USER|>{question}?<|ASSISTANT|>"

#     prompt_informed = PromptTemplate(template=template_informed, input_variables=["context", "question"])

#     return LLMChain(prompt=prompt_informed, llm=local_llm)


# def make_the_llm_ignorant():
#     if MODEL == "flan":
#         template_ignorant = """
#         when asked: {question}
#         my response is: """
#     else:
#         stablelm_system_prompt = """
#             - StableLM answers questions 
#             - If it does not have the information, StableLM answers with 'I do not know'
#         """
#         template_ignorant  = f"<|SYSTEM|>{stablelm_system_prompt}"+"<|USER|>{question}?<|ASSISTANT|>"

#     prompt_ignorant = PromptTemplate(template=template_ignorant, input_variables=["question"])

#     return LLMChain(prompt=prompt_ignorant, llm=local_llm)


def prompt(question, template=None):
    #prompt = PromptTemplate(template=template, input_variables=["question"])
    #llm_chain = LLMChain(prompt=prompt, llm=local_llm)
    response = local_llm(question)
    # print(response)
    return str(response)
