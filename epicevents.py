import click
import sentry_sdk
import utils.sentry_events
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from decouple import config


SENTRY_DSN = config('DNS_SENTRY')


sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)

from commands.login import login
from commands.logout import logout
from commands.createuser import createuser
from commands.updateuser import updateuser
from commands.createclient import createclient
from commands.getclients import getclients
from commands.updateclient import updateclient
from commands.createcontract import createcontract
from commands.getcontracts import getcontracts
from commands.updatecontract import updatecontract
from commands.createevent import createevent
from commands.getevents import getevents
from commands.updateevent import updateevent
from commands.deleteuser import deleteuser
from commands.filtercontracts import filtercontracts
from commands.filterevents import filterevents


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(createuser)
cli.add_command(logout)
cli.add_command(createclient)
cli.add_command(getclients)
cli.add_command(createcontract)
cli.add_command(getcontracts)
cli.add_command(createevent)
cli.add_command(getevents)
cli.add_command(updateclient)
cli.add_command(updatecontract)
cli.add_command(updateevent)
cli.add_command(updateuser)
cli.add_command(deleteuser)
cli.add_command(filtercontracts)
cli.add_command(filterevents)

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        click.secho(f"❌ Erreur capturée par Sentry : {e}", fg="red")
