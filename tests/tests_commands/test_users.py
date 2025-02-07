import pytest
from click.testing import CliRunner
from commands.login import login
from commands.createuser import createuser
from commands.updateuser import updateuser
from commands.deleteuser import deleteuser
from models import User, CustomGroup
from utils.db_session import get_session
from utils.password import verify_password, set_password

@pytest.fixture
def runner():
    return CliRunner()

def test_createuser_sad_path(runner):
    result = runner.invoke(login, input="support@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(createuser, input="")
    assert "Vous n'avez pas la permission de créer un utilisateur." in result.output

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(createuser, input="support@test.com\n")
    assert "Un utilisateur avec l'email support@test.com existe déjà." in result.output

    result = runner.invoke(createuser, input="newuser@test.com\npassword1234\npassword1234\nEMP001\n")
    assert "Un utilisateur avec le numéro d'employé EMP001 existe déjà." in result.output

def test_createuser_happy_path(runner):
    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(createuser, input="newuser@test.com\npassword1234\npassword1234\nEMP005\nPrénom\nNom\n1\n")
    assert "Utilisateur Prénom Nom créé avec succès" in result.output

    with get_session() as session:
        user = session.query(User).filter_by(email="newuser@test.com").first()
        assert verify_password("password1234", user.password)
        assert user.employee_number == "EMP005"
        assert user.last_name == "Nom"
        assert user.first_name == "Prénom"
        session.delete(user)
        session.commit()

def test_deleteuser(runner):
    with get_session() as session:
        support_group = session.query(CustomGroup).filter_by(name="Support").first()
        user = User(
            email="newuser@test.com",
            employee_number="EMP005",
            first_name="Prénom",
            last_name="Nom",
            password=set_password("password1234"),
            custom_group=support_group
        )
        session.add(user)
        session.commit()

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(deleteuser, args="newuser@test.com", input="y\n")
    assert "L'utilisateur a été supprimé !" in result.output

    with get_session() as session:
        assert not session.query(User).filter_by(email="newuser@test.com").first()

def test_updateuser(runner):
    with get_session() as session:
        support_group = session.query(CustomGroup).filter_by(name="Support").first()
        user = User(
            email="newuser@test.com",
            employee_number="EMP005",
            first_name="Prénom",
            last_name="Nom",
            password=set_password("password1234"),
            custom_group=support_group
        )
        session.add(user)
        session.commit()

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(updateuser, args="newuser@test.com", input="updateduser@test.com\nNew prénom\nNew nom\n"
                                                                      "EMP006\nn\n")
    assert "Les informations de l'utilisateur New prénom New nom " in result.output

    with get_session() as session:
        user = session.query(User).filter_by(email="updateduser@test.com").first()
        assert user.first_name == "New prénom"
        assert user.last_name == "New nom"
        assert user.employee_number == "EMP006"
        session.delete(user)
        session.commit()







