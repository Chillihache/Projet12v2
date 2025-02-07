import pytest
import click
from click.testing import CliRunner
from commands.login import login
from commands.logout import logout
from commands.createclient import createclient
from commands.updateclient import updateclient
from commands.getclients import getclients
from models import Client
from utils.db_session import get_session

@pytest.fixture
def runner():
    return CliRunner()


def test_getclients(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(getclients, input="")
    assert "Liste des clients" in result.output


def test_createclient_updateclient_happy_path(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(
        createclient,
        input="Prénom\nNom\nprenom.nom@test.com\nEntreprise test\n"
    )
    assert "Le client a été créé avec succès !" in result.output

    with get_session() as session:
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        assert client.first_name == "Prénom"
        assert client.last_name == "Nom"

    result = runner.invoke(updateclient,
                           args=["prenom.nom@test.com"],
                           input="New prénom\nNew nom\nprenom.nom@test.com\nNew entreprise test\n")
    assert "Le client a été modifé avec succès !" in result.output

    with get_session() as session:
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        assert client.first_name == "New prénom"
        assert client.last_name == "New nom"
        session.delete(client)
        session.commit()


def test_createclient_updateclient_no_permission(runner):
    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(createclient, input="")

    assert "Vous n'avez pas la permission de créer un client." in result.output

    result = runner.invoke(updateclient, args=["random.email@test.com"])

    assert "Vous n'avez pas la permission de modifier un client." in result.output


def test_updateclient_invalid_email(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(updateclient, args=["invalid.email@test.com"])

    assert "Le client n'existe pas." in result.output








