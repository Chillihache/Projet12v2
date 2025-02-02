from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history
import sentry_sdk
from sentry_sdk import capture_message
from models import User, Contract


def sentry_alert_user_saved(mapper, connection, target):

    session = Session.object_session(target)
    if session is None:
        return

    if session.new and target in session.new:
        action = "créé"
        capture_message(f"Le collaborateur {target.first_name} {target.last_name} a été {action}")
        sentry_sdk.flush()
        return

    modified_fields = []
    for field in target.__table__.columns.keys():
        history = get_history(target, field)
        if history.has_changes():
            modified_fields.append(field)

    if modified_fields:
        action = "modifié"
        capture_message(
            f"Le collaborateur {target.first_name} {target.last_name} a été {action}. Champs modifiés : {', '.join(modified_fields)}")
        sentry_sdk.flush()

event.listen(User, "after_insert", sentry_alert_user_saved)
event.listen(User, "after_update", sentry_alert_user_saved)


def sentry_alert_contract_signed(mapper, connection, target):
    history = get_history(target, "is_signed")

    if history.has_changes():
        old_value, new_value = history.deleted, history.added

        if old_value and not old_value[0] and new_value and new_value[0]:
            capture_message(f"Le contrat {target.contract_number} a été signé.")
            sentry_sdk.flush()

event.listen(Contract, "before_update", sentry_alert_contract_signed)




