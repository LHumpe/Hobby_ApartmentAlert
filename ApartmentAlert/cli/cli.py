import click
from ._search import startAgent

@click.group()
def cli():
    """
    This function serves as the entry point for the cli and all its sub-commands.
    :return: None
    """
    pass

cli.add_command(startAgent)
