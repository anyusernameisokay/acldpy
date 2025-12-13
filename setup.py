from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


setup(
    name='acld',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.1',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
