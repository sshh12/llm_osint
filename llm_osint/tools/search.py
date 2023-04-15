from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

from llm_osint import cache_utils


class GoogleSerperSearchWrapper(GoogleSerperAPIWrapper):
    @cache_utils.cache_func
    def run(self, query: str) -> str:
        return super().run(query)

    def _parse_results(self, results: dict) -> str:
        snippets = []

        if results.get("answerBox"):
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                return answer_box.get("answer")
            elif answer_box.get("snippet"):
                return answer_box.get("snippet").replace("\n", " ")
            elif answer_box.get("snippetHighlighted"):
                return ", ".join(answer_box.get("snippetHighlighted"))

        if results.get("knowledgeGraph"):
            kg = results.get("knowledgeGraph", {})
            title = kg.get("title")
            entity_type = kg.get("type")
            if entity_type:
                snippets.append(f"{title}: {entity_type}.")
            description = kg.get("description")
            if description:
                snippets.append(description)
            for attribute, value in kg.get("attributes", {}).items():
                snippets.append(f"{title} {attribute}: {value}.")

        for result in results["organic"][: self.k]:
            if "snippet" in result:
                snippets.append(f'{result["title"]}: {result["snippet"]} (link {result["link"]})')
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f'{result["title"]}: {attribute} = {value}.')

        if len(snippets) == 0:
            return "No good results found"

        return "\n\n".join(snippets)


def get_search_tool(**kwargs) -> Tool:
    search = GoogleSerperSearchWrapper(**kwargs)
    return Tool(
        name="Search Term",
        func=search.run,
        description="useful for when you need to find information about general things, names, usernames, places, etc. the input should be a search term",
    )
