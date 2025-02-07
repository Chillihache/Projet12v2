import pytest
from click.testing import CliRunner
import datetime
from commands.login import login
from commands.logout import logout
from commands.getevents import getevents
from commands.filterevents import filterevents
from commands.createevent import createevent
from commands.updateevent import updateevent
from commands.createclient import createclient
from models import Contract, Client, Event, User
from utils.db_session import get_session


@pytest.fixture
def runner():
    return CliRunner()

def test_getevents(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(getevents, input="")
    assert "Liste des événements" in result.output

def test_filterevents(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(filterevents, input="")
    assert "Vous n'avez pas la permission de filtrer les événements." in result.output

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(filterevents, input="")
    assert "Liste des événements" in result.output

    result = runner.invoke(login, input="support@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(filterevents, input="")
    assert "Liste des événements" in result.output

def test_createevent_happy_path(runner):
    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(
        createclient,
        input="Prénom\nNom\nprenom.nom@test.com\nEntreprise test\n"
    )
    assert "Le client a été créé avec succès !" in result.output

    with get_session() as session:
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        contract = Contract(
            contract_number="ABC123TEST",
            total_amount=100,
            remaining_amount=50,
            is_signed=True,
            client=client
        )
        session.add(contract)
        session.commit()

    result = runner.invoke(login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(
        createevent,
        input="Evenement test\n1\n2025-02-07 14:00\n2025-02-07 15:00\n1\nParis\n50\nNotes test\n"
    )
    assert "Evénement créé avec succès !" in result.output

    with get_session() as session:
        event = session.query(Event).filter_by(name="Evenement test").first()
        assert event.date_start == datetime.datetime(2025, 2, 7, 14, 0)
        assert event.location == "Paris"
        assert event.notes == "Notes test"


        session.delete(event)
        contract = session.query(Contract).filter_by(contract_number="ABC123TEST").first()
        session.delete(contract)
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        session.delete(client)
        session.commit()

def test_updateevent_happy_path(runner):
    with get_session() as session:
        sales_user = session.query(User).filter_by(email="sales@test.com").first()
        support_user = session.query(User).filter_by(email="support@test.com").first()
        client = Client(
            first_name="Prénom",
            last_name="Nom",
            email="prenom.nom@test.com",
            sales_contact=sales_user,
            company_name="Entreprise test"
        )
        session.add(client)
        contract = Contract(
            contract_number="ABC123TEST",
            total_amount=100,
            remaining_amount=50,
            is_signed=True,
            client=client
        )
        session.add(contract)
        event = Event(
            name="Evenement test",
            date_start = datetime.datetime(2025, 2, 7, 14, 0),
            date_end = datetime.datetime(2025, 2, 7, 15, 0),
            location = "Paris",
            attendees = 50,
            notes = "Notes test",
            contract = contract
        )
        session.add(event)
        session.commit()

    result = runner.invoke(login, input="management@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(updateevent, args=["Evenement test"], input="1\n")
    assert "Contact support modifié avec succès !" in result.output
    with get_session() as session:
        event = session.query(Event).filter_by(name="Evenement test").first()
        assert event.support_contact
        event.support_contact = support_user
        session.commit()

    result = runner.invoke(login, input="support@test.com\npassword123")
    assert "Connexion réussie" in result.output

    result = runner.invoke(updateevent, args=["Evenement test"],
                           input="New evenement test\nn\nMarseille\n20\nNew notes test\n")
    assert "L'Evénement a été modifié avec succès !" in result.output

    with get_session() as session:
        event = session.query(Event).filter_by(name="New evenement test").first()
        assert event.location == "Marseille"
        assert event.attendees == 20
        assert event.notes == "New notes test"
        contract = session.query(Contract).filter_by(contract_number="ABC123TEST").first()
        client = session.query(Client).filter_by(email="prenom.nom@test.com").first()
        session.delete(event)
        session.delete(contract)
        session.delete(client)
        session.commit()











