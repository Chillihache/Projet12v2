import click
import sentry_sdk
from utils.jw_tokens import delete_tokens_file


@click.command()
def logout():
    try:
        if delete_tokens_file():
            click.secho("Déconnection réussie !", fg="green")
        else:
            click.secho("Vous êtes déjà déconnecté.", fg="yellow")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()