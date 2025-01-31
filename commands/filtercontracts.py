import click
from rich.console import Console
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from utils.create_table import create_contracts_table
from models import Contract


@click.command()
def filtercontracts():
    user = authenticate_user()
    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with get_session() as session:
        user = session.merge(user)
        if "filter_contracts" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de filtrer les contrats.", fg="red")
            return

        console = Console()

        click.echo("Choisissez votre filtre :\n"
                   "1 - Contrats non signés \n"
                   "2 - Contrats non réglés \n")

        while True:
            filter_choice = click.prompt("Votre choix")

            try:
                filter_choice = int(filter_choice)
                if filter_choice in (1, 2):
                    break
            except ValueError:
                pass
            click.secho("Choix invalide.", fg="red")

        if filter_choice == 1:
            contracts = session.query(Contract).filter_by(is_signed=False)
        else:
            contracts = session.query(Contract).filter(Contract.remaining_amount > 0).all()

        table = create_contracts_table(contracts)
        console.print(table)

