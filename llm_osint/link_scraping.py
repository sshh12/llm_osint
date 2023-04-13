from typing import List
import requests
import os
from bs4 import BeautifulSoup

from llm_osint import cache_utils


@cache_utils.cache_func
def scrape_text(url: str) -> str:
    resp = requests.get(
        url="https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": os.environ["SCRAPINGBEE_API_KEY"],
            "url": url,
            "premium_proxy": "true",
            "country_code": "us",
        },
    )
    return resp.text


def _element_to_text(element) -> str:
    elem_text = element.get_text()
    lines = (line.strip() for line in elem_text.splitlines())
    parts = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(c for c in parts if c)
    return text


def _chunk_element(element, max_size: int) -> List[str]:
    text = _element_to_text(element)
    if len(text) == 0:
        return []
    if len(text) <= max_size:
        return [text]
    else:
        chunks = []
        for child in element.findChildren(recursive=False):
            chunks.extend(_chunk_element(child, max_size))
        return chunks


def _merge_text_chunks(vals: List[str], max_size: int) -> List[str]:
    combined_strings = []
    current_string = ""

    for s in vals:
        if len(current_string) + len(s) <= max_size:
            current_string += s
        else:
            combined_strings.append(current_string)
            current_string = s

    if current_string:
        combined_strings.append(current_string)

    return combined_strings


def chunk_and_strip_html(raw_html: str, max_size: int) -> List[str]:
    soup = BeautifulSoup(raw_html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    chunks = _chunk_element(soup, max_size)
    chunks = _merge_text_chunks(chunks, max_size)
    return chunks
