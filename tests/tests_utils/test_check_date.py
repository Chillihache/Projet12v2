import pytest
from click import exceptions
from utils.check_date import prompt_for_date
from datetime import datetime


def test_prompt_for_date_valid_date(mocker):
    mocker.patch("click.prompt", return_value="2025-02-04 15:30")

    result = prompt_for_date("Entrez une date :")
    expected = datetime(2025, 2, 4, 15, 30)

    assert result == expected


def test_prompt_for_date_invalid_date(mocker):
    mock_prompt = mocker.patch("click.prompt", side_effect=["invalid-date", "2025-02-04 15:30"])
    mock_click_secho = mocker.patch("click.secho")

    result = prompt_for_date("Entrer une date :")
    expected = datetime(2025, 2, 4, 15, 30)

    assert result == expected
    assert mock_prompt.call_count == 2
    mock_click_secho.assert_called_once_with("Format invalide. Veuillez entrer une date au format 'YYYY-MM-DD HH:MM'.",
                                             fg="red")


