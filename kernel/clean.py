import pandas as pd

from loguru import logger
from pathlib import Path



@logger.catch
def excel_to_csv (excel_file, csv_file):
    dataframe = pd.read_excel(excel_file, sheet_name = "دیده بان بازار")
    
    nrows = len(dataframe.index)

    if nrows < 3:
        excel_file.unlink()

        logger.warning(f"Removed {excel_file.name}.")

        return False
    
    dataframe.to_csv(csv_file)

    logger.success(f"Converted {excel_file.name}.")
    
    return True


@logger.catch
def clean (stage_dir: str, datalake_dir: str, delete_excels: bool) -> None:
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

    logger.success("Converted all excel files!")

    if delete_excels:
        for excel_file in excel_files:
            excel_file.unlink()

    logger.success("Deleted all excel files!")