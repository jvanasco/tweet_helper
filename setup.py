import os
import re
from setuptools import setup
from setuptools import find_packages

# store version in the init.py
with open(
        os.path.join(
            os.path.dirname(__file__),
            'tweet_helper.py')) as v_file:
    VERSION = re.compile(
        r".*__VERSION__ = '(.*?)'",
        re.S).match(v_file.read()).group(1)

here = os.path.abspath(os.path.dirname(__file__))
README = ""
README = README.split("\n\n", 1)[0] + "\n"

setup(
    name='tweet_helper',
    author='Jonathan Vanasco',
    author_email='jonathan@findmeon.com',
    version=VERSION,
    url='https://github.com/jvanasco/tweet_helper',
    py_modules=['tweet_helper'],
    description='twython wrapper to simplify tweeting from the commandline',
    long_description=README,
    zip_safe=False,
    keywords="",
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'twython',
        'future',  # used to standardize `input`
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Intended Audience :: Developers",
    ],
    license='MIT',
)
