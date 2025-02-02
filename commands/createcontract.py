import click
import sentry_sdk
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from models import Contract, Client


@click.command()
def createcontract():
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with get_session() as session:
            user = session.merge(user)
            if "add_contract" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de créer un contrat.", fg="red")
                return

            click.echo("Veuillez renseigner les champs suivants pour la création du contrat :")

            contract_number = click.prompt("Numéro de contrat").upper()

            if session.query(Contract).filter_by(contract_number=contract_number).first():
                click.secho("Un contrat avec ce numéro existe déjà.", fg="red")
                return

            clients = session.query(Client).all()
            clients_str = list(clients)
            click.echo("Veuillez choisir un client :")
            for i, client_str in enumerate(clients_str, start=1):
                click.echo(f"{i}. {client_str}")

            client_choice = None
            while client_choice not in range(1, len(clients) + 1):
                try:
                    client_choice = int(click.prompt("Entrez le numéro du client", type=int))
                    if client_choice not in range(1, len(clients) + 1):
                        click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez choisir un client.", fg="red")

            client = clients[client_choice - 1]

            total_amount = None
            while total_amount is None:
                try:
                    total_amount = click.prompt("Montant total")
                    total_amount = float(total_amount)
                    if len(str(total_amount).split(".")[1]) > 2:
                        click.secho("Le montant doit comporter au maximum deux chiffres après la virgule.", fg="red")
                        total_amount = None
                except ValueError:
                    click.secho("Montant incorrect", fg="red")
                    total_amount = None

            remaining_amount = None
            while remaining_amount is None:
                try:
                    remaining_amount = click.prompt("Montant restant")
                    remaining_amount = float(remaining_amount)
                    if len(str(remaining_amount).split(".")[1]) > 2:
                        click.secho("Le montant doit comporter maximum deux chiffres après la virgule.", fg="red")
                        remaining_amount = None
                except ValueError:
                    click.secho("Montant incorrect", fg="red")
                    remaining_amount = None

            is_signed = click.confirm("Le contrat est-il signé ?", default=False)

            new_contract = Contract(
                contract_number=contract_number,
                client=client,
                total_amount=total_amount,
                remaining_amount=remaining_amount,
                is_signed=is_signed
            )

            session.add(new_contract)
            session.commit()
            click.secho("Le contrat a été créé avec succès !", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
