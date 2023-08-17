from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

LLMModel = BaseChatModel

default_fast_llm_options = dict(model_name="gpt-3.5-turbo-16k-0613", request_timeout=120, max_retries=10, temperature=0.7)
default_llm_options = dict(model_name="gpt-4-0613", request_timeout=120, max_retries=10, temperature=0.7)


def get_default_fast_llm() -> LLMModel:
    chat = ChatOpenAI(**default_fast_llm_options)
    return chat


def get_default_llm() -> LLMModel:
    chat = ChatOpenAI(**default_llm_options)
    return chat
