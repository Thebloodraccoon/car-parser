import asyncio

from app.scraper.http_client import get_car_brands
from app.scraper.scraper import run


async def main():
    makes = await get_car_brands()

    # if need your list of makes, because from get car 11000 makes
    # example list of makes
    # makes = ['AUDI', 'TOYOTA', 'Mercedes-Benz', 'BMW', 'HONDA']

    threads = 5
    name = "Autoria"
    site = "https://auto.ria.com"

    await run(site, name, threads, makes)


if __name__ == "__main__":
    asyncio.run(main())
