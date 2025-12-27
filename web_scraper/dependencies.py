from basics.type_safety.pydantic_utils import TextModelRequest
from fastapi import Body
from loguru import logger

from .scraper import extract_urls, fetch_all


async def get_urls_content(body: TextModelRequest = Body(...)):
    urls = extract_urls(body.prompt)
    if urls:
        try:
            urls_content = await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warning(f"Failed to fetch some urls, Error {e}")

    return ""
