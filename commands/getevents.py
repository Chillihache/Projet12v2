import click
import sentry_sdk
from rich.console import Console
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from utils.create_table import create_events_table
from models import Event


@click.command()
def getevents():
    try:
        user = authenticate_user()
        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with get_session() as session:
            user = session.merge(user)
            if "view_events" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de voir les événements.", fg="red")
                return

            events = session.query(Event).all()
            console = Console()
            table = create_events_table(events)

            console.print(table)

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()