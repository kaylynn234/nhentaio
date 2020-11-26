# Nhentaio
An asynchronous, read-only nhentai API wrapper for the damned, depraved, and disillusioned.

## But why?
You can blame @AbstractUmbra for this one. This is entirely his fault. I had absolutely nothing to do with it.

## Installation
To install from PyPi:

```sh
# Adjust based on your environment - you may want "py" instead of "python3" on windows
python3 -m pip install nhentaio
```


If you do not value your safety - nor your sanity - you can install directly from the master branch.
```sh
# Adjust based on your environment - you may want "py" instead of "python3" on windows
python3 -m pip install git+https://github.com/kaylynn234/nhentaio
```

If you're managing your project with Poetry, you can use the following:
```sh
poetry add nhentaio
```

Do note that nhentaio requires recent-ish versions of `aiohttp`, `python-dateuti` and `lxml` to be installed. More information can be found in `requirements.txt` or `pyproject.toml`. Using Poetry has the advantage of managing venvs and dependencies for you.

Nhentaio requires Python 3.7 or later.


## Quickstart
Here's a quick example to get you going.
```py
client = nhentaio.Client()

# Put a 6 digit ID of your choice here - I'm not giving you any ideas.
gallery = await client.fetch_gallery(...)

for page in gallery.pages:
    await page.save(f"{gallery.name}_{page.number}.png")
```

## Documentation
Documentation can be found at <https://nhentaio.readthedocs.io/>.
At present there's no examples directory, but the documentation should be easy enough to follow.

## What do you mean "API"?
Nhentai technically doesn't have a public front-facing API for other services to use.
As such, getting results out of nhentai requires a more barbaric approach: web scraping.
This library employs heavy use of the Xpath specification for that purpose.
As long as nhentai doesn't change anything too drastically - which they tend not to do - this library should keep working.
If for some reason it does break, or the behavior you receive is unexpected, please open an issue or a PR.