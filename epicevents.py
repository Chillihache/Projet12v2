from utils.db_session import get_session
import click
from commands.login import login
from commands.createuser import createuser

session = get_session()


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(createuser)

if __name__ == "__main__":
    cli()
