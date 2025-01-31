import click
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from models import Client


@click.command()
def createclient():
    user = authenticate_user()

    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with get_session() as session:
        user = session.merge(user)
        if "add_client" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de créer un client.", fg="red")
            return

        click.echo("Veuillez renseigner les champs suivants pour la création du client :")

        first_name = click.prompt("Prénom")
        last_name = click.prompt("Nom")

        email = None
        while not email:
            email = click.prompt("Email")
            if session.query(Client).filter_by(email=email).first():
                click.secho("Cette email est déjà utilisé par un client.", fg="red")
                email = None

        company_name = click.prompt("Nom de l'entreprise")

        new_client = Client(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            company_name=company_name,
                            sales_contact=user
                            )

        session.add(new_client)
        session.commit()
        click.secho("Le client a été créé avec succès !", fg="green")
