import jdatetime
import requests

from loguru import logger
from pathlib import Path
from typing import Tuple

URL = "http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d={year}-{month}-{day}"


@logger.catch
def remove_holidays (start_date: Tuple[int, int, int], end_date: Tuple[int, int, int]) -> jdatetime.date:
    start_date = jdatetime.date(*start_date)
    end_date = jdatetime.date(*end_date)

    while start_date <= end_date:
        if start_date.weekday() < 5:
            yield start_date

        start_date += jdatetime.timedelta(days = 1)


@logger.catch
def fetch_excel (date: jdatetime.date, stage_dir: Path) -> None:
    try:
        respone = requests.get(
            URL.format(
                year = date.year,
                month = date.month,
                day = date.day
            )
        )
    except Exception as e:
        logger.error(f"An error occurred during fetching excel file: {e}")

    name = f"{date.year}-{date.month:02}-{date.day:02}"
    excel_path = stage_dir / f"{name}.xlsx"
    
    try:
        with excel_path.open("wb") as handler:
            handler.write(respone.content)
    except Exception as e:
        logger.error(f"An error occurred during saving excel file: {e}")
    
    logger.info(f"Fetched {name}.")


@logger.catch
def download_excels (start_date: Tuple[int, int, int], end_date: Tuple[int, int, int], stage_dir: str) -> jdatetime.date:
    dates = remove_holidays(start_date, end_date)

    stage_dir = Path(stage_dir)
    stage_dir.mkdir(parents = True, exist_ok = True)

    for date in dates:
        fetch_excel(date, stage_dir)
    
    logger.success("Everything has been fetched successfully.")