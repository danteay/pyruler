"""Package definition."""

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyruler',
    version='0.11.1',
    packages=find_packages(),
    description='Simple and powerful python rule engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/danteay/pyruler.git',
    author='Eduardo Aguilar',
    author_email='dante.aguilar41@gmail.com',
    keywords=['rule', 'engine', 'ruler' 'package'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
