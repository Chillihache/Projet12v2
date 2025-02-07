import pytest
from click.testing import CliRunner
from commands.login import login
from commands.logout import logout
from commands.getcontracts import getcontracts
from commands.createcontract import createcontract
from commands.updatecontract import updatecontract
from commands.filtercontracts import filtercontracts
from commands.createclient import createclient
from models import Contract, Client
from utils.db_session import get_session


@pytest.fixture
def runner():
    return CliRunner()

def test_getcontracts(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(getcontracts, input="")
    assert "Liste des contrats" in result.output

def test_filtercontracts_happy_path(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(filtercontracts, input="1")
    assert "Liste des contrats" in result.output

    result = runner.invoke(filtercontracts, input="2")
    assert "Liste des contrats" in result.output

def test_filtercontracts_no_permissions(runner):
    result = runner.invoke(login, input="support@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(filtercontracts, input="1")
    assert "Vous n'avez pas la permission de filtrer les contrats." in result.output

def test_createcontract_updatecontract_happy_path(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(
        createclient,
        input="Prénom\nNom\nprenom.nom@test.com\nEntreprise test\n"
    )
    assert "Le client a été créé avec succès !" in result.output

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(
        createcontract,
        input="ABC123TEST\n1\n100.00\n50.00\nn\n"
    )

    assert "Le contrat a été créé avec succès !" in result.output

    with get_session() as session:
        contract = session.query(Contract).filter_by(contract_number="ABC123TEST").first()
        assert contract.total_amount == 100
        assert contract.remaining_amount == 50
        assert not contract.is_signed

    result = runner.invoke(updatecontract,
                           args=["ABC123TEST"],
                           input="ABC123TEST2\n25\n10\ny\nn\n")

    assert "Le contrat a été modifié avec succès !" in result.output

    with get_session() as session:
        contract = session.query(Contract).filter_by(contract_number="ABC123TEST2").first()
        assert contract.total_amount == 25
        assert contract.remaining_amount == 10
        assert contract.is_signed
        session.delete(contract)
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        session.delete(client)
        session.commit()




