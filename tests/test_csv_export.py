import csv
import pytest

from spendsense import csv_export


def test_csv_export(tmp_path, monkeypatch):

    sample_expenses = [
        {
            "id": 1,
            "date": "2026-11-01",
            "category": "Food",
            "amount": "250.00",
            "note": "Lunch"
        }
    ]

    monkeypatch.setattr(
        csv_export,
        "get_expenses_by_month",
        lambda month: sample_expenses
    )

    monkeypatch.setattr(
        csv_export,
        "EXPORT_DIR",
        tmp_path
    )

    file_path = csv_export.export_monthly_expenses("2026-11")

    assert file_path.exists()

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["category"] == "Food"
    assert rows[0]["amount"] == "250.00"


def test_csv_export_empty_month(tmp_path, monkeypatch):

    monkeypatch.setattr(
        csv_export,
        "get_expenses_by_month",
        lambda month: []
    )

    monkeypatch.setattr(
        csv_export,
        "EXPORT_DIR",
        tmp_path
    )

    with pytest.raises(ValueError):

        csv_export.export_monthly_expenses("2026-11")


def test_csv_export_invalid_month():

    with pytest.raises(ValueError):

        csv_export.export_monthly_expenses("November-2026")