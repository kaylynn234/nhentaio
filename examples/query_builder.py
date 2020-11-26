# Example #3: query_builder.py


import asyncio
import nhentaio


async def main():
    client = nhentaio.Client()

    # Since these methods return the class instance, fluid-style chaining is possible.
    query = nhentaio.Query().add("yaoi", "full color", "english", "males only").exclude("shotacon")

    # If you have a lengthier query, you can do it the boring way:
    another_query = nhentaio.Query()
    another_query.add("yaoi", "full color", "english", "males only")
    another_query.exclude("shotacon")
    # You can also limit based on page count
    another_query.pages(20)
    # As well as upload date - this will only return galleries uploaded in the last 5 hours
    another_query.uploaded(nhentaio.Days(5))

    # If need be, you can easily copy queries like so
    yet_another_query = another_query.copy()
    # You can also use ranges for page counts/upload dates
    yet_another_query.pages(less_than=50, more_than=20)
    yet_another_query.uploaded(less_than=nhentaio.Years(3), more_than=nhentaio.Days(5))

    # Queries can be passed to the search function as you'd expect
    async for result in client.search(yet_another_query):
        print(result.title)

asyncio.get_event_loop().run_until_complete(main())