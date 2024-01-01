from setuptools import setup, find_packages

setup(
    name="python_serverless_housefire",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-dotenv",
        "requests",
        "undetected-chromedriver",
    ],
)
