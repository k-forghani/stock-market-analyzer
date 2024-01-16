import jdatetime

import rich_click as click
from loguru import logger

import kernel
import generic


# References:
# https://click.palletsprojects.com/en/8.1.x/options/
# https://github.com/ewels/rich-click

logger.add("error.log", filter = lambda record: record["level"].name == "ERROR")
logger.add("info.log", filter = lambda record: record["level"].name != "ERROR")

click.rich_click.USE_MARKDOWN = True

CONTEXT_SETTINGS = dict(help_option_names = ["-h", "--help"])


@click.group(
    context_settings = CONTEXT_SETTINGS,
    epilog = "",
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


@cli.command(
    context_settings = CONTEXT_SETTINGS,
    epilog = ""
)
@click.option(
    "--stage-directory",
    required = True,
    prompt = "Enter stage directory",
    type = click.Path(exists = False, file_okay = False, dir_okay = True),
    help = "Stage directory"
)
@click.option(
    "--start-date",
    default = (jdatetime.date.today() - jdatetime.timedelta(days = 7)).strftime("%Y-%m-%d"),
    show_default = True,
    prompt = "Enter the start date",
    type = click.UNPROCESSED,
    callback = generic.validate_date,
    help = "Start date"
)
@click.option(
    "--end-date", "-nd",
    default = jdatetime.date.today().strftime("%Y-%m-%d"),
    show_default = True,
    prompt = "Enter the end date",
    type = click.UNPROCESSED,
    callback = generic.validate_date,
    help = "End date"
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
    epilog = ""
)
@click.option(
    "--stage-directory",
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
    help = "Datalake directory"
)
@click.option(
    "--clean-stage",
    is_flag = True,
    default = True,
    show_default = True,
    prompt = "Clean stage or not",
    help = "Clean stage or not"
)
def convert (*args, **kwargs):
    """Converting data.
    """

    logger.info(f"Config: {kwargs}")

    kernel.convert.convert(
        stage_dir = kwargs["stage_directory"],
        datalake_dir = kwargs["datalake_directory"],
        clean_stage = kwargs["clean_stage"]
    )


@cli.command(
    context_settings = CONTEXT_SETTINGS,
    epilog = ""
)
@click.option(
    "--datalake-directory",
    required = True,
    prompt = "Enter datalake directory",
    type = click.Path(exists = False, file_okay = False, dir_okay = True),
    help = "Datalake directory"
)
def analyze (*args, **kwargs):
    """Analyzing data.
    """

    logger.info(f"Config: {kwargs}")

    kernel.analyze.analyze(
        datalake_dir = kwargs["datalake_directory"]
    )


if __name__ == "__main__":
    cli()