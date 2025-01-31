import click
from rich.console import Console
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from utils.create_table import create_clients_table
from models import Client


@click.command()
def getclients():
    user = authenticate_user()
    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with get_session() as session:
        user = session.merge(user)
        if "view_clients" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de voir les client.", fg="red")
            return

        clients = session.query(Client).all()
        console = Console()
        table = create_clients_table(clients)

        console.print(table)