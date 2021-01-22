import os
import re
from setuptools import setup
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

long_description = (
    description
) = "twython wrapper to simplify tweeting from the commandline"
with open(os.path.join(HERE, "README.md")) as r_file:
    long_description = r_file.read()

# store version in the init.py
with open(os.path.join(HERE, "tweet_helper.py")) as v_file:
    VERSION = (
        re.compile(r".*__VERSION__ = \"(.*?)\"", re.S).match(v_file.read()).group(1)
    )

setup(
    name="tweet_helper",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    version=VERSION,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvanasco/tweet_helper",
    py_modules=["tweet_helper"],
    zip_safe=False,
    keywords="",
    test_suite="tests",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["twython", "certifi"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
    license="MIT",
    # scripts=['tweet_helper.py'],  # this works, but creates a tweet_helper.py ; we can lose the .py if we use an entrypoint to create the shim
    entry_points={"console_scripts": ["tweet_helper=tweet_helper:go_commandline"]},
)
