import click
from utils.jw_tokens import authenticate_user
from utils.db_session import get_session
from models import User, CustomGroup
from utils.password import set_password


@click.command()
def createuser():
    user = authenticate_user()
    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with get_session() as session:
        user = session.merge(user)

        if "add_user" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de créer un utilisateur.", fg="red")
            return

        try:
            groups = session.query(CustomGroup).all()
            if not groups:
                click.secho(
                    "Aucun groupe disponible. Veuillez d'abord configurer les groupes.",
                    fg="yellow",
                )
                return
            del groups[2]

            click.echo("Veuillez renseigner les informations suivantes :")
            email = click.prompt("Email")
            if session.query(User).filter_by(email=email).first():
                click.secho(f"Un utilisateur avec l'email {email} existe déjà.", fg="red")
                return

            password = click.prompt(
                "Mot de passe",
                hide_input=True,
                confirmation_prompt="Veuillez répéter le mot de passe pour confirmation",
            )

            employee_number = click.prompt("Numéro d'employé")
            if session.query(User).filter_by(employee_number=employee_number).first():
                click.secho(
                    f"Un utilisateur avec le numéro d'employé {employee_number} existe déjà.",
                    fg="red",
                )
                return

            first_name = click.prompt("Prénom")
            last_name = click.prompt("Nom")

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

            group = groups[group_choice - 1]

            new_user = User(
                email=email,
                employee_number=employee_number,
                first_name=first_name,
                last_name=last_name,
                password=set_password(password),
                custom_group=group
            )

            session.add(new_user)
            session.commit()

            click.secho(
                f"Utilisateur {first_name} {last_name} créé avec succès et ajouté au groupe {group.name} !",
                fg="green",
            )

        except Exception as e:
            session.rollback()
            click.secho(f"Erreur lors de la création de l'utilisateur : {e}", fg="red")


