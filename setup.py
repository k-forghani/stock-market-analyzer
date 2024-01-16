from setuptools import setup

# https://click.palletsprojects.com/en/8.1.x/setuptools/#scripts-in-packages

setup(
    name = "stock-market-analyzer",
    version = "1.0.0",
    py_modules = ["kernel"],
    install_requires = [
        "click",
        "rich-click",
        "tqdm",
        "loguru",
        "jdatetime"
    ],
    entry_points = {
        "console_scripts": [
            "stock = cli:cli",
        ]
    }
)
