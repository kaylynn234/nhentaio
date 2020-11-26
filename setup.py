import re
import setuptools


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open("README.md") as f:
    readme = f.read()


with open("nhentaio/__init__.py") as f:
    version = re.search(r'__version__ = "([\d\.]+)"', f.read(), re.MULTILINE)[1]


setuptools.setup(
    name="nhentaio",
    author="Kaylynn",
    url="https://github.com/kaylynn234/nhentaio/",
    project_urls={
        "Documentation": "https://nhentaio.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/kaylynn234/nhentaio/issues",
    },
    version=version,
    packages=["nhentaio"],
    license="MIT",
    description="An asynchronous, read-only nhentai API wrapper for the damned, depraved, and disillusioned.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
    ]
)