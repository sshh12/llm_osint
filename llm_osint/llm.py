from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

LLMModel = BaseChatModel

# GPT-5-era models run on the Responses API and reject a custom `temperature`
# and `stop` sequences, so neither is set here (the tool-calling agent in
# web_agent.py drives the model with native function calling, not stop tokens).
default_fast_llm_options = dict(model="gpt-5.4-mini", request_timeout=120, max_retries=10)
default_llm_options = dict(model="gpt-5.5", request_timeout=120, max_retries=10)


def get_default_fast_llm() -> LLMModel:
    return ChatOpenAI(**default_fast_llm_options)


def get_default_llm() -> LLMModel:
    return ChatOpenAI(**default_llm_options)
