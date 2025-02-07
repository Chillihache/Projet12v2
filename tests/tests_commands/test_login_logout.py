import pytest
from click.testing import CliRunner
from commands import login, logout

@pytest.fixture
def runner():
    return CliRunner()

def test_login_invalid_email(runner):
    result = runner.invoke(login.login, input="invalid_email@test.com")
    assert "Utilisateur inconnu." in result.output

def test_login_invalid_password(runner):
    result = runner.invoke(login.login, input="sales@test.com\nwrongpassword")
    assert "Mot de passe incorrect." in result.output

def test_login_valid(runner):
    result = runner.invoke(login.login, input="sales@test.com\npassword123")
    assert "Connexion réussie" in result.output

def test_logout(runner):
    runner.invoke(login.login, input="sales@test.com\npassword123")
    result = runner.invoke(logout.logout)
    assert "Déconnection réussie !" in result.output
