# Example #2: search.py


import asyncio
import nhentaio


async def main():
    client = nhentaio.Client()

    # You can search with a string as you would on the website
    async for result in client.search('"full color"'):
        print(result.title)

    # By default, only 25 results are returned. You can use the limit kwarg to change that.
    async for result in client.search("translated", limit=100):
        print(result.title)

    # You can also change the sorting method
    async for result in client.search("english", limit=10, sort_by=nhentaio.SortType.popular_this_week):
        print(result.title)

    # Valid options are:
    # SortType.recent
    # SortType.popular_today
    # SortType.popular_this_week
    # SortType.popular_this_month

    # SortType.recent is the default.
    # See the documentation for more details.

    # If you'd like, you can also flatten your search results into a list, instead of using an async iterator.
    # results = await client.search("english", limit=10).flatten()

    # Be careful! If there are no search results, an error will be raised.
    try:
        results = await client.search("goijigoeujhogehgoehjg", limit=10).flatten()
    except nhentaio.NotFound:
        print("Oops!")

    # Filtering results is also possible, and works similarly to Python's normal filter function.
    # First you need a predicate:
    def short_title(item: nhentaio.PartialGallery):
        return len(item.title) < 30

    # And then you can filter like so.
    # Note that flattening is not required - you could use "async for" normally if you wanted to.
    results = await client.search("english", limit=10).filter(short_title).flatten()
    print(f"I found {len(results)} with a short title!")

asyncio.get_event_loop().run_until_complete(main())