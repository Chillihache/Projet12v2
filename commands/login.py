import click
import sentry_sdk
from sqlalchemy.exc import NoResultFound
from utils.jw_tokens import save_tokens, generate_tokens
from utils.password import verify_password
from utils.db_session import get_session
from models import User


@click.command()
def login():
    try:
        with get_session() as session:

            email = click.prompt("Email")

            try:
                user = session.query(User).filter_by(email=email).one()

            except NoResultFound:
                click.secho("Utilisateur inconnu.", fg="red")
                return

            password = click.prompt("Mot de passe", hide_input=True)

            if verify_password(password, user.password):
                access_token, refresh_token = generate_tokens(email, password)

                save_tokens(access_token, refresh_token)

                click.secho("Connexion réussie", fg="green")

            else :
                click.secho("Mot de passe incorrect.", fg="red")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()