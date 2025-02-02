import click
import sentry_sdk
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from models import Client


@click.command()
@click.argument("email")
def updateclient(email):
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with get_session() as session:
            user = session.merge(user)
            if "change_client" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de modifier un client.", fg="red")
                return

            client = session.query(Client).filter_by(email=email).first()

            if not client:
                click.secho("Le client n'existe pas.", fg="red")
                return

            if user != client.sales_contact:
                click.secho("Vous n'êtes pas en charge de ce client.", fg="red")
                return

            click.echo(f"Modification des informations du client {client.first_name} {client.last_name}.\n"
                       f"Laissez vides les champs que vous ne souhaitez pas modifier")

            new_first_name = click.prompt("Nouveau prénom", default=client.first_name)
            new_last_name = click.prompt("Nouveau nom de famille", default=client.last_name)

            new_email = None
            while not new_email:
                new_email = click.prompt("Nouvel email", default=client.email)
                if session.query(Client).filter_by(email=new_email).first():
                    if new_email != client.email:
                        click.secho("Cette email est déjà utilisé par un client.", fg="red")
                        new_email = None
            new_company_name = click.prompt("Nouveau nom d'entrepirse", default=client.company_name)

            client.first_name = new_first_name
            client.last_name = new_last_name
            client.email = new_email
            client.company_name = new_company_name

            session.commit()

            click.secho("Le client a été modifé avec succès !", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()