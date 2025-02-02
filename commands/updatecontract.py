import click
import sentry_sdk
from sqlalchemy.orm import joinedload
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from models import Contract, Client, CustomGroup, User


@click.command()
@click.argument("contract_number")
def updatecontract(contract_number):
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with (get_session() as session):
            user = session.merge(user)
            if "change_contract" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de modifier un contrat.", fg="red")
                return

            contract_number.upper()
            contract = session.query(Contract).options(joinedload(Contract.client)).filter_by(contract_number=contract_number).first()

            if not contract:
                click.secho("Ce contrat n'existe pas.", fg="red")
                return

            user_is_sales = session.query(CustomGroup).join(User.custom_group).filter(CustomGroup.name == "Sales",
                                                                                      User.id == user.id).first()

            if user_is_sales and user != contract.client.sales_contact:
                click.secho("Vous n'êtes pas en charge de ce contrat.", fg="red")
                return

            click.echo(f"Modification des informations du contrat {contract_number}.\n"
                       f"Laissez vides les champs que vous ne souhaitez pas modifier.")

            new_contract_number = None
            while not new_contract_number:
                new_contract_number = click.prompt("Nouveau numéro de contrat", default=contract.contract_number).upper()
                if session.query(Contract).filter_by(contract_number=new_contract_number).first():
                    if new_contract_number != contract.contract_number:
                        click.secho("Ce numéro de contrat existe déjà", fg="red")
                        new_contract_number = None

            new_total_amount = None
            while new_total_amount is None:
                try:
                    new_total_amount = click.prompt("Nouveau montant total", default=contract.total_amount)
                    new_total_amount = float(new_total_amount)
                    if len(str(new_total_amount).split(".")[1]) > 2:
                        click.secho("Le montant doit comporter maximum deux chiffres après la virgule.", fg="red")
                        new_total_amount = None
                except ValueError:
                    click.secho("Montant incorrect.", fg="red")
                    new_total_amount = None

            new_remaining_amount = None
            while new_remaining_amount is None:
                try:
                    new_remaining_amount = click.prompt("Nouveau montant restant", default=contract.remaining_amount)
                    new_remaining_amount = float(new_remaining_amount)
                    if len(str(new_remaining_amount).split(".")[1]) > 2:
                        click.secho("Le montant doit comporter maximum deux chiffres après la virgule.", fg="red")
                        new_remaining_amount = None
                except ValueError:
                    click.secho("Montant incorrect", fg="red")
                    new_remaining_amount = None

            new_is_signed = click.confirm("Le contrat est-il signé ?", default=contract.is_signed)

            client_choice = click.confirm(f"Le client lié au contrat est {contract.client}. Souhaitez-vous le modifier ?")

            if client_choice:
                clients = session.query(Client).all()
                click.echo("Veuillez choisir un client :")
                clients_str = list(clients)
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

                new_client = clients[client_choice - 1]

            else:
                new_client = contract.client

            contract.contract_number = new_contract_number
            contract.total_amount = new_total_amount
            contract.remaining_amount = new_remaining_amount
            contract.is_signed = new_is_signed
            contract.client = new_client

            session.commit()

            click.secho(f"Le contrat a été modifié avec succès !", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()




