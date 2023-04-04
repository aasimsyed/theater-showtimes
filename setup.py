from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="theater-showtimes",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "theater-showtimes=src.theater_showtimes:main",
        ],
    },
    author="Aasim Syed",
    author_email="aasim.ss@gmail.com",
    description="A project for calculating and displaying movie theater showtimes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)
