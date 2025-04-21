import asyncio

from app.scraper.scraper import run


async def main():
    # if need your list of makes take to this list
    makes = ["AUDI", "TOYOTA", "Mercedes-Benz", "BMW", "HONDA", "RENO", "FIAT"]

    threads = 40
    site = "autobazar" # or autoria

    await run(
        site=site,
        threads=threads,
        makes=makes,
    )


if __name__ == "__main__":
    asyncio.run(main())
