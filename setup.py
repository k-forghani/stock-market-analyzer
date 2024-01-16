from setuptools import setup

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