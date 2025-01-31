import click
from utils.db_session import get_session
from utils.jw_tokens import authenticate_user
from models import User


@click.command()
@click.argument("email")
def deleteuser(email):
    user = authenticate_user()

    if not user:
        click.secho("Authentification échouée.", fg="red")
        return

    with (get_session() as session):
        user = session.merge(user)
        if "delete_user" not in user.get_permissions(session):
            click.secho("Vous n'avez pas la permission de supprimer un utilisateur.", fg="red")
            return

        user_to_delete = session.query(User).filter_by(email=email).first()

        if not user_to_delete:
            click.secho("Cet email ne correspond a aucun utilisateur.", fg="red")
            return

        if not click.confirm(f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user_to_delete.first_name} {user_to_delete.last_name} ?"):
            click.secho("Suppression annulée.", fg="yellow")
            return

        session.delete(user_to_delete)
        session.commit()

        click.secho("L'utilisateur a été supprimé !", fg="green")