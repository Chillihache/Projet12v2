import click
from utils.jw_tokens import delete_tokens_file


@click.command()
def logout():
    if delete_tokens_file():
        click.secho("Déconnection réussie !", fg="green")
    else:
        click.secho("Vous êtes déjà déconnecté.", fg="yellow")