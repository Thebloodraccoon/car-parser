import asyncio
import logging
import sys
import traceback
from typing import Dict, List

from http_client import get_car_brands, get_content
from parsers import parse_data, transform_make_for_source
from data_processors import process_car_data
from utils import chunk_list

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("parser.log")],
)
logger = logging.getLogger(__name__)


async def process_make(
    base_url: str, site_name: str, make: str, semaphore: asyncio.Semaphore
) -> Dict[str, int]:
    """Process a single make with semaphore control."""
    results = {"processed": 0, "saved": 0, "errors": 0}

    async with semaphore:
        try:
            logger.info(f"Processing make: {make}")
            source_make = transform_make_for_source(make)
            content = await get_content(base_url, source_make)

            if not content:
                logger.warning(f"No content found for make: {make}")
                return results

            cars = parse_data(content, site_name, make, base_url)
            results["processed"] = len(cars)

            for car_data in cars:
                try:
                    saved = await process_car_data(car_data)
                    if saved:
                        results["saved"] += 1
                except Exception as e:
                    error_details = traceback.format_exc()
                    logger.error(
                        f"Error processing car for make {make}: {e}\n{error_details}"
                    )
                    results["errors"] += 1

            logger.info(
                f"Completed processing make {make}. Processed: {results['processed']}, Saved: {results['saved']}, Errors: {results['errors']}"
            )
            return results

        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Error processing make {make}: {e}\n{error_details}")
            results["errors"] += 1
            return results


async def process_makes_chunk(
    base_url: str, site_name: str, makes_chunk: List[str], semaphore: asyncio.Semaphore
) -> Dict[str, int]:
    """Process a chunk of makes."""
    tasks = []
    results = {"processed": 0, "saved": 0, "errors": 0}

    for make in makes_chunk:
        task = asyncio.create_task(process_make(base_url, site_name, make, semaphore))
        tasks.append(task)

    make_results = await asyncio.gather(*tasks)

    for result in make_results:
        results["processed"] += result["processed"]
        results["saved"] += result["saved"]
        results["errors"] += result["errors"]

    return results


async def run_parser(base_url: str, site_name: str, threads: int = 5, makes: List[str] = None) -> Dict[str, int]:
    """Run a parser with specified number of threads."""
    try:
        logger.info("Getting car makes...")

        if not makes:
            logger.error("No makes found to process")
            return {"processed": 0, "saved": 0, "errors": 0}

        logger.info(f"Found {len(makes)} makes to process")

        chunk_size = max(1, round(len(makes) / threads))
        make_chunks = chunk_list(makes, chunk_size)

        logger.info(
            f"Processing makes in {len(make_chunks)} chunks with {threads} threads"
        )

        semaphore = asyncio.Semaphore(threads)

        tasks = []
        for chunk in make_chunks:
            task = asyncio.create_task(
                process_makes_chunk(base_url, site_name, chunk, semaphore)
            )
            tasks.append(task)

        chunk_results = await asyncio.gather(*tasks)

        total_results = {"processed": 0, "saved": 0, "errors": 0}
        for result in chunk_results:
            total_results["processed"] += result["processed"]
            total_results["saved"] += result["saved"]
            total_results["errors"] += result["errors"]

        logger.info(
            f"Parser run completed. Processed: {total_results['processed']}, Saved: {total_results['saved']}, Errors: {total_results['errors']}"
        )
        return total_results
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error running parser for {site_name}: {e}\n{error_details}")
        return {"processed": 0, "saved": 0, "errors": 1}


async def run(base_url: str, site_name: str, threads: int = 5, makes: List[str] = None):
    """Run the parser with the given parameters."""
    try:
        logger.info(f"Starting parser for site: {site_name}")
        results = await run_parser(base_url, site_name, threads, makes)
        logger.info(f"Parser for {site_name} completed with results: {results}")
        return results
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error running parser for {site_name}: {e}\n{error_details}")
        return {"processed": 0, "saved": 0, "errors": 1}


