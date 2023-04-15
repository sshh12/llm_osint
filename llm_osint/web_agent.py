from typing import List, Optional

from langchain.agents import Tool
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent import AgentExecutor
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from llm_osint import llm, web_agent_constants


def build_web_agent(tools: List[Tool], memory: Optional[BaseChatMemory] = None, **custom_agent_kwargs) -> AgentExecutor:
    agent_kwargs = {
        "prefix": web_agent_constants.PREFIX,
        "suffix": web_agent_constants.SUFFIX,
        "format_instructions": web_agent_constants.FORMAT_INSTRUCTIONS,
    }
    if memory is None:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_kwargs.update(custom_agent_kwargs)
    agent_chain = initialize_agent(
        tools,
        llm.get_default_llm(),
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        agent_kwargs=agent_kwargs,
    )
    return agent_chain
