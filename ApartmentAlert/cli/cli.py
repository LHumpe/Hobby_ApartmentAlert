import click
from ._search import _start_Agent

@click.group()
def cli():
    """
    This function serves as the entry point for the cli and all its sub-commands.
    :return: None
    """
    pass

cli.add_command(_start_Agent)