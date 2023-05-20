"""
Module that defines common utility methods.
"""

import asyncio
import aiohttp


async def fetch_urls_json_data(urls):
    """Fetches JSON data from multiple URLs asynchronously.

    Args:
        urls (List[str]): List of URLs from which to fetch JSON data.

    Returns:
        list: List of JSON responses obtained from the URLs.
    """

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(session.get(url, ssl=False))
        responses = await asyncio.gather(*tasks)
        json_responses = []
        for response in responses:
            json_responses.append(await response.json())
        return json_responses
