import pandas as pd

from loguru import logger
from pathlib import Path


@logger.catch
def excel_to_csv (excel_file: Path, csv_file: Path) -> bool:
    try:
        dataframe = pd.read_excel(
            excel_file,
            sheet_name = "دیده بان بازار",
            header = 2
        )
    except Exception as e:
        raise Exception(f"An error occurred during opening the excel file: {e}")
    
    nrows = len(dataframe.index)

    if nrows < 3:
        excel_file.unlink()

        logger.warning(f"Deleted {excel_file.name}.")

        return False
    
    try:
        dataframe.to_csv(csv_file)
    except Exception as e:
        raise Exception(f"An error occurred during saving the file: {e}")

    logger.log(f"Converted {excel_file.name}.")
    
    return True


@logger.catch
def clean (stage_dir: str, datalake_dir: str, clean_stage: bool) -> None:
    stage_dir = Path(stage_dir)
    if not stage_dir.is_dir():
        raise Exception("Not a directory!")
    
    datalake_dir = Path(datalake_dir)
    datalake_dir.mkdir(parents = True, exist_ok = True)

    excel_files = stage_dir.glob("*.xlsx")

    excel_files = [
        excel_file for excel_file in excel_files
        if excel_to_csv(
            excel_file,
            datalake_dir / excel_file.with_suffix(".csv").name
        )
    ]

    logger.log("Converted all excel files into csv files.")

    if clean_stage:
        for excel_file in excel_files:
            excel_file.unlink()

    logger.log("Deleted all excel files.")