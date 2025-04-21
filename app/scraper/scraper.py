import asyncio
import traceback
from typing import Dict, List

from app.scraper.parsers.factory import create_parser
from app.scraper.utils.logger import setup_logger
from app.scraper.utils.utils import chunk_list, process_car_data

logger = setup_logger("app.scraper")


async def process_make(parser, make, semaphore: asyncio.Semaphore) -> Dict[str, int]:
    """Process a single make with semaphore control."""
    results = {"processed": 0, "saved": 0, "errors": 0}

    make_name = make.get("title") if isinstance(make, dict) else make

    async with semaphore:
        try:
            logger.info(f"Processing make: {make_name}")
            content = await parser.get_content(make)

            if not content:
                logger.warning(f"No content found for make: {make_name}")
                return results

            cars = parser.parse_data(content, make)
            results["processed"] = len(cars)

            for car_data in cars:
                try:
                    saved = await process_car_data(car_data)
                    if saved:
                        results["saved"] += 1
                except Exception as e:
                    logger.error(f"Error processing car for make {make_name}: {e}")
                    results["errors"] += 1

            logger.info(
                f"Completed processing make {make_name}. Processed: {results['processed']}, "
                f"Saved: {results['saved']}, Errors: {results['errors']}"
            )
            return results

        except Exception as e:
            logger.error(f"Error processing make {make_name}: {e}\n")
            results["errors"] += 1
            return results


async def process_makes_chunk(
    parser, makes_chunk: List[str], semaphore: asyncio.Semaphore
) -> Dict[str, int]:
    """Process a chunk of makes."""
    tasks = []
    results = {"processed": 0, "saved": 0, "errors": 0}

    for make in makes_chunk:
        task = asyncio.create_task(process_make(parser, make, semaphore))
        tasks.append(task)

    make_results = await asyncio.gather(*tasks)

    for result in make_results:
        results["processed"] += result["processed"]
        results["saved"] += result["saved"]
        results["errors"] += result["errors"]

    return results


async def run_parser(
    parser, threads: int = 5, makes: List[str] = None
) -> Dict[str, int]:
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
            task = asyncio.create_task(process_makes_chunk(parser, chunk, semaphore))
            tasks.append(task)

        chunk_results = await asyncio.gather(*tasks)

        total_results = {"processed": 0, "saved": 0, "errors": 0}
        for result in chunk_results:
            total_results["processed"] += result["processed"]
            total_results["saved"] += result["saved"]
            total_results["errors"] += result["errors"]

        logger.info(
            f"Parser run completed. Processed: {total_results['processed']} Saved: {total_results['saved']}, Errors: {total_results['errors']}"
        )
        return total_results
    except Exception as e:
        logger.error(f"Error running parser: {e}")
        return {"processed": 0, "saved": 0, "errors": 1}


async def run(
    site: str,
    threads: int = 5,
    makes: List[str] = [],
):
    """Run the parser with the given parameters."""
    try:
        logger.info(f"Starting parser for site: {site}")

        parser = create_parser(site)
        site_name = parser.site_name
        if not parser:
            logger.error(f"No parser implementation found for site type: {site_name}")
            return {"processed": 0, "saved": 0, "errors": 1}

        makes = await parser.get_car_brands(makes)

        results = await run_parser(parser, threads, makes)
        logger.info(f"Parser for {site_name} completed with results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error running parser for {site_name}: {e}")
        return {"processed": 0, "saved": 0, "errors": 1}
