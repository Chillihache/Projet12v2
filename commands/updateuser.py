import click
import sentry_sdk
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from utils.password import set_password
from models import User, CustomGroup


@click.command()
@click.argument("email")
def updateuser(email):
    try:
        user = authenticate_user()

        if not user:
            click.secho("Authentification échouée.", fg="red")
            return

        with (get_session() as session):
            user = session.merge(user)
            if "change_user" not in user.get_permissions(session):
                click.secho("Vous n'avez pas la permission de modifier un utilisateur.", fg="red")
                return

            user_to_update = session.query(User).filter_by(email=email).first()

            if not user_to_update:
                click.secho("Cet email ne correspond à aucun utilisateur.", fg="red")
                return


            groups = session.query(CustomGroup).all()
            if not groups:
                click.secho(
                    "Aucun groupe disponible. Veuillez d'abord configurer les groupes.",
                    fg="yellow",
                )
                return
            del groups[2]

            click.echo(f"Modification des informations de l'utilisateur {user_to_update.first_name} {user_to_update.last_name}.\n"
                       "Laissez vides les champs que vous ne souhaitez pas modifier.")

            new_email = None
            while not new_email:
                new_email = click.prompt("Nouvel email", default=user_to_update.email)
                if session.query(User).filter_by(email=new_email).first():
                    if new_email != user_to_update.email:
                        click.secho("Cet email est déjà utilisé par un autre utilisateur.", fg="red")
                        new_email = None

            new_first_name = click.prompt("Nouveau prénom", default=user_to_update.first_name)
            new_last_name = click.prompt("Nouveau nom", default=user_to_update.last_name)

            new_password = click.prompt("Nouveau mot de passe (laisser vide pour ne pas changer)",
                                        default="",
                                        hide_input=True,
                                        confirmation_prompt="Veuillez répéter le mot de passe pour confirmation")

            new_employee_number = None
            while not new_employee_number:
                new_employee_number = click.prompt("Nouveau numéro d'employé", default=user_to_update.employee_number)
                if session.query(User).filter_by(employee_number=new_employee_number).first():
                    if new_employee_number != user_to_update.employee_number:
                        click.secho("Ce numéro d'employé est déjà utilisé par un autre utilisateur.", fg="red")
                        new_employee_number = None

            modify_user_group = click.confirm("Souhaitez-vous modifier le département de l'utiliseteur ?")

            if modify_user_group:
                click.echo("Veuillez choisir un département :")
                for i, group in enumerate(groups, start=1):
                    click.echo(f"{i}. {group.name}")

                group_choice = None
                while group_choice not in range(1, len(groups) + 1):
                    try:
                        group_choice = int(click.prompt("Entrez le numéro du groupe", type=int))
                        if group_choice not in range(1, len(groups) + 1):
                            click.secho(
                                "Choix invalide. Veuillez sélectionner un numéro valide.", fg="red"
                            )
                    except ValueError:
                        click.secho("Entrée invalide. Veuillez choisir un département.", fg="red")

                new_group = groups[group_choice - 1]
                user_to_update.custom_group = new_group


            user_to_update.email = new_email
            user_to_update.first_name = new_first_name
            user_to_update.last_name = new_last_name
            user_to_update.employee_number = new_employee_number
            if new_password:
                new_password = set_password(new_password)
                user_to_update.password = new_password

            session.commit()

            click.secho(f"Les informations de l'utilisateur {user_to_update.first_name} {user_to_update.last_name} ont été mises à jour avec succès.", fg="green")

    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
