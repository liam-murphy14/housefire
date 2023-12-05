from setuptools import setup, find_packages

setup(
    name="python_scripts_housefire",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "redis",
        "hiredis",
        "python-dotenv",
        "requests",
        "undetected-chromedriver",
    ],
)
