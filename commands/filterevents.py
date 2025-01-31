import click
from rich.console import Console
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from utils.create_table import create_events_table
from models import Event


@click.command()
def filterevents():
    user = authenticate_user()

    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with (get_session() as session):
        user = session.merge(user)
        if "filter_events" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de filtrer les événements.", fg="red")
            return

        console = Console()

        if user.custom_group.name == "Support":
            events = session.query(Event).filter(Event.support_contact == user).all()

        elif user.custom_group.name == "Management":
            events = session.query(Event).filter(Event.support_contact_id.is_(None)).all()
        else:
            click.secho("Vous n'êtes ni dans le département gestion ni dans le département support, "
                       "vous ne pouvez pas filtrer les événements.", fg="red")
            return

        table = create_events_table(events)
        console.print(table)