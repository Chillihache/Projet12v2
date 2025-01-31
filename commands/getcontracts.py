import click
from rich.console import Console
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from utils.create_table import create_contracts_table
from models import Contract


@click.command()
def getcontracts():
    user = authenticate_user()
    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with get_session() as session:
        user = session.merge(user)
        if "view_contracts" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de voir les contrats.", fg="red")
            return

    contracts = session.query(Contract).all()
    console = Console()
    table = create_contracts_table(contracts)

    console.print(table)