import pandas as pd

from loguru import logger
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown


console = Console()


class CSV:
    def __init__ (self, path):
        if not isinstance(path, Path):
            path = Path(path)
        
        if not path.is_file():
            raise FileNotFoundError(f"File doesn't exist: {path}")
        
        try:
            self.dataframe = pd.read_csv(path)
        except Exception as e:
            raise Exception(f"An error occurred during opening the csv file: {e}")
    
    def get_max_turnover (self, number = 10):
        try:
            result = self.dataframe.nlargest(number, columns = ["حجم"])
            result = result[["نماد", "حجم"]]
            return result.to_markdown(index = False)
        except Exception as e:
            logger.error(f"An error occurred during analysis: {e}")
    
    def get_highest_price_growth (self):
        try:
            result = self.dataframe.nlargest(1, columns = ["قیمت پایانی - تغییر"])
            return result.to_markdown(index = False)
        except Exception as e:
            logger.error(f"An error occurred during analysis: {e}")
    
    def get_highest_price_drop (self):
        try:
            result = self.dataframe.nsmallest(1, columns = ["قیمت پایانی - تغییر"])
            return result.to_markdown(index = False)
        except Exception as e:
            logger.error(f"An error occurred during analysis: {e}")


@logger.catch
def analyze (datalake_dir: str) -> None:
    datalake_dir = Path(datalake_dir)
    if not datalake_dir.is_dir():
        raise ValueError(f"Not a directory: {datalake_dir}")
    
    csv_files = datalake_dir.glob("*.csv")

    for csv_file in csv_files:
        csv_object = CSV(csv_file)

        console.print(
            Markdown(f"# روز {csv_file.stem}")
        )

        console.print(
            Markdown("## ۱۰ نماد با بیشتر حجم\n\n" + csv_object.get_max_turnover())
        )
        console.print(
            Markdown("## بیشترین رشد قیمت\n\n" + csv_object.get_highest_price_growth())
        )
        console.print(
            Markdown("## بیشترین افت قیمت\n\n" + csv_object.get_highest_price_drop())
        )

        logger.info(f"Analyzed {csv_file.stem}.")
    
    logger.success("Everything has been analyzed.")