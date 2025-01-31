from rich.table import Table


def create_events_table(events):
    table = Table(title="Liste des événements")

    table.add_column("Nom")
    table.add_column("Contrat")
    table.add_column("Date de début")
    table.add_column("Date de fin")
    table.add_column("Contact support")
    table.add_column("Adresse")
    table.add_column("Nombre d'invités")
    table.add_column("Informations supplémentaires")

    for event in events:
        contrat_str = str(event.contract) if event.contract else "Non attribué"
        support_contact_str = str(event.support_contact) if event.support_contact else "Non assigné"
        attendees_str = str(event.attendees)

        table.add_row(event.name, contrat_str, event.date_start.strftime("%Y-%m-%d %H:%M:%S"),
                      event.date_end.strftime("%Y-%m-%d %H:%M:%S"), support_contact_str,
                      event.location, attendees_str, event.notes)

    return table


def create_contracts_table(contracts):
    table = Table(title="Liste des contrats")

    table.add_column("Numéro de contrat")
    table.add_column("Client")
    table.add_column("Montant total")
    table.add_column("Montant restant")
    table.add_column("Date de création")
    table.add_column("Etat")

    for contract in contracts:
        client_str = str(contract.client) if contract.client else "Non attribué"
        state = "Signé" if contract.is_signed else "Non signé"

        total_amount_str = f"{contract.total_amount:.2f}" if contract.total_amount else "0.00"
        remaining_amount_str = f"{contract.remaining_amount:.2f}" if contract.remaining_amount else "0.00"

        table.add_row(contract.contract_number, client_str, total_amount_str, remaining_amount_str,
                      contract.creation_date.strftime("%Y-%m-%d %H:%M:%S"), state)

    return table


def create_clients_table(clients):
    table = Table(title="Liste des clients")

    table.add_column("Nom")
    table.add_column("Prénom")
    table.add_column("Email")
    table.add_column("Nom de l'entreprise")
    table.add_column("Date de création")
    table.add_column("Date de dernière modification")
    table.add_column("Contact commercial")

    for client in clients:
        sales_contact_str = str(client.sales_contact) if client.sales_contact else "Non attribué"
        table.add_row(client.last_name, client.first_name, client.email, client.company_name,
                      client.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                      client.update_date.strftime("%Y-%m-%d %H:%M:%S"), sales_contact_str)

    return table