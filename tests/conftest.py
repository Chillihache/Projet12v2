import pytest
import os
from models import User, CustomGroup
from utils.db_session import get_session
from utils.password import set_password

@pytest.fixture(scope="session", autouse=True)
def setup_test_users():
    session = get_session()
    try:
        sales_group = session.query(CustomGroup).filter_by(name="Sales").first()
        support_group = session.query(CustomGroup).filter_by(name="Support").first()
        management_group = session.query(CustomGroup).filter_by(name="Management").first()

        test_users = [
            User(
                email="sales@test.com",
                password=set_password("password123"),
                employee_number="EMP001",
                first_name="Sales",
                last_name="User",
                custom_group=sales_group
            ),
            User(
                email="support@test.com",
                password=set_password("password123"),
                employee_number="EMP002",
                first_name="Support",
                last_name="User",
                custom_group=support_group
            ),
            User(
                email="management@test.com",
                password=set_password("password123"),
                employee_number="EMP003",
                first_name="Management",
                last_name="User",
                custom_group=management_group
            )
        ]

        session.add_all(test_users)
        session.commit()
        print("Les utilisateurs de test ont été créés.")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création des utilisateurs de test : {e}")

    yield

    try:
        session.query(User).filter(User.email.in_([
            "sales@test.com",
            "support@test.com",
            "management@test.com"
        ])).delete(synchronize_session='fetch')
        session.commit()
        print("Les utilisateurs de test ont été supprimés.")

        token_file = "jw_tokens.json"
        if os.path.exists(token_file):
            os.remove(token_file)

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression des utilisateurs de test : {e}")

    finally:
        session.close()
