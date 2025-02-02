import click
import sentry_sdk
from utils.db_session import get_session
from utils.check_date import prompt_for_date
from utils.jw_tokens import authenticate_user
from models import Event, Contract, Client, CustomGroup, User



@click.command()
def createevent():
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with get_session() as session:
            user = session.merge(user)
            if "add_event" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de créer un événement.", fg="red")
                return

            click.echo("Veuillez renseigner les champs suivants pour la création de l'événement :")

            name = click.prompt("Nom").upper()

            if session.query(Event).filter_by(name=name).first():
                click.secho("Il existe déjà un événement avec ce nom.", fg="red")
                return

            contracts = session.query(Contract).join(Client).filter(
                Contract.is_signed == True,
                Client.sales_contact == user
            ).all()

            if len(contracts) == 0:
                click.secho("Aucun contrat disponibles. (non signés)", fg="red")
                return

            click.echo("Veuillez choisir un contrat (contrats signés uniquement) :")
            contrats_str = list(contracts)
            for i, contrats_str in enumerate(contrats_str, start=1):
                click.echo(f"{i}. {contrats_str}")

            contract_choice = None

            while contract_choice not in range(1, len(contracts) + 1):
                try:
                    contract_choice = int(click.prompt("Entrez le numéro du contrat", type=int))
                    if contract_choice not in range(1, len(contracts) + 1):
                        click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez choisir un contrat.", fg="red")

            contract = contracts[contract_choice - 1]

            date_start = prompt_for_date("Date de début (format: YYYY-MM-DD HH:MM)")
            date_end = prompt_for_date("Date de fin (format: YYYY-MM-DD HH:MM)")

            group_support = session.query(CustomGroup).filter_by(name="Support").first()
            if group_support:
                supports = session.query(User).join(User.custom_group).filter(CustomGroup.id == group_support.id).all()
            else:
                supports = []

            if len(supports) == 0:
                click.secho("Aucun collaborateur dans le département support. Le champ 'Contact Support' restera vide.", fg="yellow")
                support_contact = None
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

            location = click.prompt("Adresse")

            while True:
                try:
                    attendees = int(click.prompt("Nombre d'invités"))
                    if attendees >= 1:
                        break
                    else:
                        click.secho("Le nombre d'invités doit être égal ou supérieur à 1.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez entrer un nombre entier.", fg="red")

            notes = click.prompt("Informations supplémentaires (Peut être laissé vide)", default="", show_default=False)

            new_event = Event(
                name=name,
                contract = contract,
                date_start=date_start,
                date_end=date_end,
                support_contact = support_contact,
                location=location,
                attendees=attendees,
                notes=notes
            )

            session.add(new_event)
            session.commit()
            click.secho("Evénement créé avec succès !", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
