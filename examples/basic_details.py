# Example #1: basic_details.py


import asyncio
import nhentaio


async def main():
    client = nhentaio.Client()

    gallery = await client.random_gallery()
    print(gallery.title)

    for tag in gallery.tags:
        print(f"{tag.name}: {tag.count}")


asyncio.get_event_loop().run_until_complete(main())