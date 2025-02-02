import click
import sentry_sdk
from datetime import datetime
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from utils.check_date import prompt_for_date
from models import Event, CustomGroup, User



@click.command()
@click.argument("name")
def updateevent(name):
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with (get_session() as session):
            user = session.merge(user)
            if "change_event" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de modifier un événement.", fg="red")
                return

            name = name.upper()
            event = session.query(Event).filter_by(name=name).first()

            if not event:
                click.secho("Cet évennement n'existe pas.", fg="red")
                return

            if user.custom_group.name == "Support" and user != event.support_contact:
                click.secho("Vous n'êtes pas en charge de cet événement.", fg="red")
                return

            if user.custom_group.name == "Management":
                group_support = session.query(CustomGroup).filter_by(name="Support").first()
                if group_support:
                    supports = session.query(User).join(User.custom_group).filter(CustomGroup.id == group_support.id).all()
                else:
                    supports = []

                if len(supports) == 0:
                    click.secho("Aucun collaborateur dans le département support.", fg="red")
                    return
                else:
                    supports = list(supports)
                    click.echo("Veuillez choisir un colaborateur du département support a affecter à l'événement :")

                    for i, support in enumerate(supports, start=1):
                        click.echo(f"{i}. {support.first_name} {support.last_name}")

                    click.secho(f"{len(supports) + 1}. Ne pas assigner de support", fg="yellow")

                    support_choice = None
                    while support_choice not in range(1, len(supports) + 2):
                        try:
                            support_choice = int(click.prompt("Votre choix", type=int))
                            if support_choice not in range(1, len(supports) + 2):
                                click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
                        except ValueError:
                            click.secho("Entrée invalide.", fg="red")

                    if support_choice == len(supports) + 1:
                        support_contact = None
                    else:
                        support_contact = supports[support_choice - 1]

                    event.support_contact = support_contact
                    session.commit()
                    click.secho("Contact support modifié avec succès !", fg="green")

            else:
                click.echo(f"Modification des informations de l'événement {event.name}.\n"
                           "Laissez vides les champs que vous ne souhaitez pas modifier.")

                new_name = None
                while not new_name:
                    new_name = click.prompt("Nouveau nom", default=event.name).upper()
                    if session.query(Event).filter_by(name=new_name).first():
                        if new_name != event.name:
                            click.secho("Ce nom d'évennement existe déjà.", fg="red")
                            new_name = None

                modify_date_choice = click.confirm("Souhaitez-vous modifier les dates de début et de fin ?")

                if modify_date_choice:
                    new_date_start = prompt_for_date("Date de début (format: YYYY-MM-DD HH:MM)")
                    new_date_end = prompt_for_date("Date de fin (format: YYYY-MM-DD HH:MM)")
                else:
                    new_date_start = event.date_start
                    new_date_end = event.date_end

                new_location = click.prompt("Nouvelle adresse", default=event.location)

                while True:
                    try:
                        new_attendees = int(click.prompt("Nouveau nombre d'invités", default=event.attendees))
                        if new_attendees >= 1:
                            break
                        else:
                            click.secho("Le nombre d'invités doit être égal ou supérieur à 1.", fg="red")
                    except ValueError:
                        click.secho("Entrée invalide. Veuillez entrer un nombre entier.", fg="red")

                new_notes = click.prompt("Nouvelles informations supplémentaires", default=event.notes)

                event.name = new_name
                event.date_start = new_date_start
                event.date_end = new_date_end
                event.location = new_location
                event.attendees = new_attendees
                event.notes = new_notes

                session.commit()

                click.secho("L'Evénement a été modifié avec succès !", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()




