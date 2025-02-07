import pytest
from rich.table import Table
from datetime import datetime
from utils.create_table import create_events_table, create_contracts_table, create_clients_table


class Event:
    def __init__(self, name, contract, date_start, date_end, support_contact, location, attendees, notes):
        self.name = name
        self.contract = contract
        self.date_start = date_start
        self.date_end = date_end
        self.support_contact = support_contact
        self.location = location
        self.attendees = attendees
        self.notes = notes


class Contract:
  def __init__(self, contract_number, client, total_amount, remaining_amount, creation_date, is_signed):
        self.contract_number = contract_number
        self.client = client
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.creation_date = creation_date
        self.is_signed = is_signed


class Client:
 def __init__(self, last_name, first_name, email, company_name, creation_date, update_date, sales_contact):
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.company_name = company_name
        self.creation_date = creation_date
        self.update_date = update_date
        self.sales_contact = sales_contact


def test_create_table():
    event = Event(
        name="Événement Test",
        contract="Contrat Test",
        date_start=datetime(2025, 2, 1, 10, 0),
        date_end=datetime(2025, 2, 1, 12, 0),
        support_contact="Support Test",
        location="Lieu Test",
        attendees=50,
        notes="Note de test"
    )

    contract = Contract(
        contract_number="12345",
        client="Client Test",
        total_amount=5000.00,
        remaining_amount=2000.00,
        creation_date=datetime(2025, 1, 15, 9, 30),
        is_signed=True
    )

    client = Client(
        last_name="Nom de famille",
        first_name="Prénom",
        email="prenom.nom@test.com",
        company_name="Entreprise Test",
        creation_date=datetime(2025, 1, 10, 8, 0),
        update_date=datetime(2025, 1, 20, 14, 30),
        sales_contact="Commercial Test"
    )

    events_table = create_events_table([event])
    assert isinstance(events_table, Table)
    assert len(events_table.rows) == 1
    assert events_table.columns[0]._cells[0] == "Événement Test"
    assert events_table.columns[1]._cells[0] == "Contrat Test"
    assert events_table.columns[4]._cells[0] == "Support Test"
    assert events_table.columns[6]._cells[0] == "50"

    contracts_table = create_contracts_table([contract])
    assert isinstance(contracts_table, Table)
    assert len(contracts_table.rows) == 1
    assert contracts_table.columns[0]._cells[0] == "12345"
    assert contracts_table.columns[1]._cells[0] == "Client Test"
    assert contracts_table.columns[5]._cells[0] == "Signé"

    clients_table = create_clients_table([client])
    assert isinstance(clients_table, Table)
    assert len(clients_table.rows) == 1
    assert clients_table.columns[2]._cells[0] == "prenom.nom@test.com"
    assert clients_table.columns[3]._cells[0] == "Entreprise Test"
