from sqlalchemy import exists
import click
from models import Base, Permission, CustomGroup, CustomGroupPermission, User, Client, Event, Contract
from utils.password import set_password
from utils.db_session import get_session


session = get_session()

# Dictionnaire des permissions pour chaque groupe
groups_permissions = {
    "SuperUser": ["view_clients", "view_contracts", "view_events", "view_users",
                  "add_user", "change_user", "delete_user",
                  "add_client", "change_client",
                  "add_event", "change_event", "filter_events",
                  "add_contract", "change_contract", "filter_contracts"],
    "Sales": ["view_clients", "view_contracts", "view_events",
              "add_client", "change_client",
              "change_contract", "filter_contracts",
              "add_event"],
    "Support": ["view_clients", "view_contracts", "view_events",
                "change_event", "filter_events"],
    "Management": ["view_clients", "view_contracts", "view_events", "view_users",
                   "add_user", "change_user", "delete_user",
                   "add_contract", "change_contract",
                   "change_event", "filter_events"]
}

# Récupération de tous les noms de permissions (pour éviter les doublons)
all_permissions_names = set()
for permissions in groups_permissions.values():
    all_permissions_names.update(permissions)

# Ajouter les permissions dans la base de données si elles n'existent pas déjà
for permission_name in all_permissions_names:
    if not session.query(Permission).filter_by(name=permission_name).first():
        permission = Permission(name=permission_name)
        session.add(permission)

# Valider les ajouts de permissions
session.commit()

# Ajout des groupes et attribution des permissions
for group_name, permissions in groups_permissions.items():
    group = session.query(CustomGroup).filter_by(name=group_name).first()
    if not group:
        group = CustomGroup(name=group_name)
        session.add(group)

    for permission_name in permissions:
        permission = session.query(Permission).filter_by(name=permission_name).first()
        if permission and not session.query(CustomGroupPermission).filter_by(custom_group_id=group.id, permission_id=permission.id).first():
            group_permission = CustomGroupPermission(custom_group=group, permission=permission)
            session.add(group_permission)

# Valider les ajouts des groupes et permissions
session.commit()

# Message de confirmation
click.secho(message="Initialisation de la base de données complète ! \n", fg="green")

# Création du superuser
click.secho(message="Création du super-utilisateur, veuillez renseigner les champs suivants :", fg="cyan", bold=True)

superuser_group = session.query(CustomGroup).filter_by(name="SuperUser").first()

email = None
while not email:
    email = click.prompt("Email")
    email_exists = session.query(exists().where(User.email==email)).scalar()
    if email_exists:
        click.secho("Un utilisateur utilise déjà cette adresse email.", fg="red")
        email = None

password = click.prompt("Mot de passe", type=str, hide_input=True,
                        confirmation_prompt="Veuillez confirmer le mot de passe")

password = set_password(password)

employee_number = None
while not employee_number:
    employee_number = click.prompt("Numéro d'employé")
    employee_number_exists = session.query(exists().where(User.employee_number==employee_number)).scalar()
    if employee_number_exists:
        click.secho("Un utilisateur utilise déjà ce numéro d'employé.", fg="red")
        employee_number = None

first_name = click.prompt("Prénom")
last_name = click.prompt("Nom")

superuser = User(
    email=email,
    password=password,
    employee_number=employee_number,
    first_name=first_name,
    last_name=last_name,
    custom_group=superuser_group
)
session.add(superuser)
session.commit()
click.secho(message="Le super-utilisateur a été créé avec succès !", fg="green")


