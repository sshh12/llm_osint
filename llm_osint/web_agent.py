from typing import List, Optional

from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from llm_osint import llm

SYSTEM_PROMPT = """You are an automated OSINT agent who can expertly find information on persons, companies, places, and things using the provided tools.

Answer the user's questions by scanning the internet for relevant data. Be very thorough.

Guidelines:
* Always read the contents of linked webpages that can give you more information to answer the query.
* Use the contents of webpages to recursively discover information; follow links that could provide more.
* If you have exhausted the obvious resources, do not stop early -- search for another detail you could learn more about.
* When you have gathered enough information, respond with a thorough write-up of everything you found."""


def build_web_agent(
    tools: List[Tool], memory: Optional[BaseChatMemory] = None, **custom_agent_kwargs
) -> AgentExecutor:
    if memory is None:
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, input_key="input", output_key="output"
        )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm.get_default_llm(), tools, prompt)
    executor_kwargs = dict(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15,
    )
    executor_kwargs.update(custom_agent_kwargs)
    return AgentExecutor(**executor_kwargs)
