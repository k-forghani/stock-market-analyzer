import rich_click as click
from loguru import logger

def validate_date (ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        year, month, day = value.split("-")
        return int(year), int(month), int(day)
    except ValueError:
        logger.error("Invalid date!")
        raise click.BadParameter("Invalid date!")