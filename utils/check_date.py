import click
from datetime import datetime


def prompt_for_date(prompt_text):
    while True:
        date_input = click.prompt(prompt_text)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            click.secho("Format invalide. Veuillez entrer une date au format 'YYYY-MM-DD HH:MM'.", fg="red")