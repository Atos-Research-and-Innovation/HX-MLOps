"""RP To-Do entry point script."""

from mlopsTool import __app_name__
from mlopsTool.cli import cli


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
