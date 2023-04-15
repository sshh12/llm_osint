from typing import List, Callable, Optional

from langchain.agents.agent import AgentExecutor
from llm_osint import knowledge_agent_constants, llm


def run_chain_with_retries(agent_chain: AgentExecutor, retries: int, **agent_run_kwargs) -> str:
    exception = None
    for _ in range(retries):
        try:
            return agent_chain.run(**agent_run_kwargs)
        except Exception as e:
            exception = e
    raise exception


def run_knowledge_agent(
    gather_prompt: str,
    build_web_agent_func: Callable[[], AgentExecutor],
    deep_dive_topics: int,
    deep_dive_rounds: int,
    retries: Optional[int] = 3,
    model: Optional[llm.LLMModel] = None,
    **prompt_args
) -> List[str]:
    if model is None:
        model = llm.get_default_llm()
    initial_agent_chain = build_web_agent_func()
    initial_info_chunk = run_chain_with_retries(
        initial_agent_chain,
        retries,
        input=knowledge_agent_constants.INITIAL_WEB_AGENT_PROMPT.format(gather_prompt=gather_prompt),
    )
    knowledge_chunks = [initial_info_chunk]
    for _ in range(deep_dive_rounds):
        round_knowlege = "\n\n".join(knowledge_chunks)
        deep_dive_area_prompt = knowledge_agent_constants.DEEP_DIVE_LIST_PROMPT.format(
            num_topics=deep_dive_topics, gather_prompt=gather_prompt, current_knowlege=round_knowlege, **prompt_args
        )
        deep_dive_list = model.call_as_llm(deep_dive_area_prompt)
        try:
            deep_dive_areas = [v.split(". ", 1)[1] for v in deep_dive_list.strip().split("\n")]
        except IndexError:
            print("Failed to parse topics", deep_dive_list)
            break
        for deep_dive_topic in deep_dive_areas:
            deep_dive_web_agent_prompt = knowledge_agent_constants.DEEP_DIVE_WEB_AGENT_PROMPT.format(
                gather_prompt=gather_prompt,
                current_knowlege=round_knowlege,
                deep_dive_topic=deep_dive_topic,
            )
            agent_chain = build_web_agent_func()
            info_chunk = run_chain_with_retries(
                agent_chain,
                retries,
                input=deep_dive_web_agent_prompt,
            )
            knowledge_chunks.append(info_chunk)
    return knowledge_chunks
