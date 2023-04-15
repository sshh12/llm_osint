from typing import Optional

from langchain.agents import Tool

from llm_osint.link_scraping import scrape_text, chunk_and_strip_html
from llm_osint.llm_map_reduce import map_reduce_texts
from llm_osint import llm


PARSE_MAP_PROMPT = """
Given this text from {link} extract key unique personal characteristics and links about {name} as a list.

Only include values if they are derived from the original text and relate to {name}.

If a link begins with "/" prefix it with {link}. Do not include links to generic website pages like login, privacy, or legal.

{example_instructions}

---
{{text}}
"""

PARSE_EXAMPLE_EXTRACTION = """
For example
- name:
- location:
- age:
- job title:
- projects:
- hobbies:
- people they know:
- common activities:
- interesting personal links:
- coworkers:
"""

PARSE_REDUCE_PROMPT = """
Given these chunks of details from {link} about {name}. Merge and duduplicate these into a single list.

If some details disagree, pick the most common one. For links, include at most 10 of the most related links.

{{texts}}
"""


class ReadLinkWrapper:
    def __init__(
        self,
        map_prompt: Optional[str] = PARSE_MAP_PROMPT,
        example_instructions: Optional[str] = PARSE_EXAMPLE_EXTRACTION,
        reduce_prompt: Optional[str] = PARSE_REDUCE_PROMPT,
        model: Optional[llm.LLMModel] = None,
        **format_kwargs
    ):
        self.model = model
        self.map_prompt = map_prompt
        self.example_instructions = example_instructions
        self.reduce_prompt = reduce_prompt
        self.format_kwargs = format_kwargs

    def run(self, query: str) -> str:
        if query.endswith(".pdf"):
            return "Cannot read links that end in pdf"
        chunks = chunk_and_strip_html(scrape_text(query), 4000)
        format_args = {**self.format_kwargs, "link": query, "example_instructions": self.example_instructions}
        return map_reduce_texts(
            chunks,
            map_prompt=self.map_prompt.format(**format_args),
            reduce_prompt=self.reduce_prompt.format(**format_args),
            reduce_chunks=100,
            model=self.model,
        )


def get_read_link_tool(**kwargs) -> Tool:
    read_link = ReadLinkWrapper(**kwargs)
    return Tool(
        name="Read Link",
        func=read_link.run,
        description="useful to read and extract the contents of any link. the input should be a valid url starting with http or https",
    )
