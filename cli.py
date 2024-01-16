from pathlib import Path

import rich_click as click
from loguru import logger

import kernel


# References:
# https://click.palletsprojects.com/en/8.1.x/options/
# https://github.com/ewels/rich-click

logger.add("error.log", filter = lambda record: record["level"].name == "ERROR")
logger.add("info.log", filter = lambda record: record["level"].name != "ERROR")

click.rich_click.USE_MARKDOWN = True

CONTEXT_SETTINGS = dict(help_option_names = ["-h", "--help"])


@click.group(
    context_settings = CONTEXT_SETTINGS,
    epilog = "Check out README.md for more details.",
    help = f"Stock Market Analyzer {kernel.__version__} ({kernel.__status__})\n\n{kernel.__copyright__} {kernel.__license__}."
)
@click.version_option(
    kernel.__version__, "-V", "--version", message = "%(prog)s, version %(version)s"
)
def cli ():
    f"""Stock Market Analyzer
    
    An analysis tool for stock market data.
    """
    pass



def validate_date (ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        year, month, day = value.split("-")
        return int(year), int(month), int(day)
    except ValueError:
        logger.error("Invalid date!")
        raise click.BadParameter("Invalid date!")



@cli.command(
    context_settings = CONTEXT_SETTINGS,
    epilog = "Check out README.md for more details."
)
@click.option(
    "--stage-directory", "-cwd",
    required = True,
    prompt = "Enter stage directory",
    type = click.Path(exists = False, file_okay = False, dir_okay = True),
    help = "Stage directory"
)
@click.option(
    "--start-date", "-sd",
    default = "1402-10-18",
    show_default = True,
    prompt = "Enter the starting date",
    type = click.UNPROCESSED,
    callback = validate_date,
    help = "Starting date"
)
@click.option(
    "--end-date", "-nd",
    default = "1402-10-24",
    show_default = True,
    prompt = "Enter the ending date",
    type = click.UNPROCESSED,
    callback = validate_date,
    help = "Ending date"
)
def fetch (*args, **kwargs):
    """Fetching data.
    """

    logger.info(f"Config: {kwargs}")

    kernel.fetch.download_excels(
        start_date = kwargs["start_date"],
        end_date = kwargs["end_date"],
        stage_dir = kwargs["stage_directory"]
    )


@cli.command(
    context_settings = CONTEXT_SETTINGS,
    epilog = "Check out README.md for more details."
)
@click.option(
    "--stage-directory", "-sd",
    required = True,
    prompt = "Enter stage directory",
    type = click.Path(exists = True, file_okay = False, dir_okay = True),
    help = "Stage directory"
)
@click.option(
    "--datalake-directory", "-dd",
    required = True,
    prompt = "Enter datalake directory",
    type = click.Path(exists = False, file_okay = False, dir_okay = True),
    help = "Datelake directory"
)
@click.option(
    "--delete-excels",
    is_flag = True,
    default = True,
    show_default = True,
    prompt = "Delete excels or not",
    help = "Delete excels or not"
)
def clean (*args, **kwargs):
    """Cleaning data.
    """

    logger.info(f"Config: {kwargs}")

    kernel.clean.clean(
        stage_dir = kwargs["stage_directory"],
        datalake_dir = kwargs["datalake_directory"],
        delete_excels = kwargs["delete_excels"]
    )


if __name__ == "__main__":
    cli()