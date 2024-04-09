from setuptools import setup, find_packages
from os import path

__version__ = 1.0

with open( ".\\readme.md", "r") as f:
    long_description = f.read()

with open(".\\requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="pytse_filter",
    version=__version__,
    author="Farhad Mohammadi",
    author_email="farhad.mohammadi60@gmail.com",
    description="A user-friendly project to filter symbols of Tehran Stock Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farhad-mohammadi/pytse_filter",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires = ">=3.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    package_data = {
        "pytse_filter": ["docs/*", "examples/*","syms.json"]
    },
    license="MIT License",
    license_file="license.md"
)
