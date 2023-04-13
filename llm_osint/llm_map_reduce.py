from typing import List, Optional

from llm_osint import cache_utils, link_scraping, llm


@cache_utils.cache_func
def map(prompt: str, text: str, model: llm.LLMModel) -> str:
    return model.call_as_llm(prompt.format(text=text))


@cache_utils.cache_func
def reduce(prompt: str, texts: List[str], model: llm.LLMModel) -> str:
    return model.call_as_llm(prompt.format(texts="\n\n".join(texts)))


def map_reduce_texts(
    texts: List[str], map_prompt: str, reduce_prompt: str, reduce_n: int, model: Optional[llm.LLMModel] = None
) -> str:
    if model is None:
        model = llm.get_default_fast_llm()

    mapped_texts = []
    for text in texts:
        mapped_texts.append(map(map_prompt, text, model))

    for text in mapped_texts:
        print()
        print(text)

    while len(mapped_texts) > 1:
        print(len(mapped_texts))
        reduce_chunks = []
        while len(mapped_texts) > 0 and len(reduce_chunks) < reduce_n:
            reduce_chunks.append(mapped_texts.pop(0))
        mapped_texts.append(reduce(reduce_prompt, reduce_chunks, model))

    return mapped_texts[0]
