import logging
from typing import Optional, List, Dict

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
from parsers import extract_ticket_items

logger = logging.getLogger(__name__)

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


async def get_car_brands() -> List[str]:
    """Get list of car brands from NHTSA API."""
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"

    response = await send_request(
        url=url,
        method="GET",
        headers=HEADERS,
    )

    data = response.json()
    makes = [make["Make_Name"] for make in data["Results"]]
    return makes


async def get_content(base_url: str, make: str, page: int = 1) -> Optional[Dict]:
    """Get content from API for a specific make and page."""
    try:
        url = f"{base_url}/uk/car/{make}/"
        response = await send_request(
            url=url,
            method="GET",
            headers=HEADERS,
            params={
                "page": page,
            },
        )

        if response and response.status_code == 200:
            html_content = response.text
            ticket_items = extract_ticket_items(html_content)

            return {"results": ticket_items}
        else:
            logger.error(
                f"Failed to get data for make {make}: {response.status_code if response else 'No response'}"
            )
            return None
    except Exception as e:
        logger.error(f"Error fetching data for make {make}: {e}")
        return None
