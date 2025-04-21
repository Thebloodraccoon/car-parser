import logging
from typing import Optional

import httpx
from tenacity import (
    after_log,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)

from app.conf import ua, PROXY
from app.scraper.utils.logger import setup_logger

logger = setup_logger("app.scraper.utils.http_client")

HEADERS = {
    "User-Agent": ua.random,
}


@retry(
    stop=stop_after_attempt(20),
    wait=wait_fixed(2),
    retry=(
        retry_if_exception_type(
            (httpx.RequestError, httpx.TimeoutException, httpx.HTTPStatusError)
        )
        | retry_if_result(
            lambda result: result is not None and result.status_code == 502
        )
    ),
    after=after_log(logger, log_level=logging.WARNING),
    reraise=True,
)
async def send_request(
    url: str,
    method: str = "GET",
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    headers: Optional[dict] = None,
    json: Optional[dict] = None,
    cookies: Optional[dict] = None,
    timeout: int = 30,
) -> Optional[httpx.Response]:
    """Send an HTTP request with retry logic."""
    proxy = f"http://{PROXY}" if PROXY else None

    if headers is None:
        headers = HEADERS.copy()

    async with httpx.AsyncClient(
        proxy=proxy, timeout=timeout, cookies=cookies, follow_redirects=True
    ) as client:
        if method.upper() == "GET":
            response = await client.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(
                url, params=params, data=data, json=json, headers=headers
            )
        else:
            raise httpx.HTTPError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()
        return response
    return None
