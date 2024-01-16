# Stock Market Analyzer

## Introduction

An analysis tool for stock market data.

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
pip3 install --editable .
```

## Documentation

```bash
stock fetch
stock convert
stock analyze
```

## Dependencies

- Python==3.11.4
    - Click==8.1.7
    - Rich-click==1.7.3
    - Loguru==0.7.2
    - jdatetime==4.1.1
    - Pandas=2.1.4
    - openpyxl=3.1.2
    - tabulate=0.9.0
    - rich==3.0.0