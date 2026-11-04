
import json
import pytest

from spendsense import budget_service as bs


@pytest.fixture
def temporary_budget_file(tmp_path, monkeypatch):
    file_path = tmp_path / "budgets.json"

    file_path.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(bs, "DATA_FILE", file_path)

    return file_path


def test_set_new_budget(temporary_budget_file):
    result = bs.set_budget("2026-11", "Food", "5000")

    assert result["month"] == "2026-11"
    assert result["category"] == "Food"
    assert result["amount"] == "5000.00"


def test_update_existing_budget(temporary_budget_file):
    bs.set_budget("2026-11", "Food", "5000")
    bs.set_budget("2026-11", "food", "6000")

    budgets = bs.load_budgets()

    assert len(budgets) == 1
    assert budgets[0]["amount"] == "6000.00"


def test_get_budget(temporary_budget_file):
    bs.set_budget("2026-11", "Food", "5000")

    assert bs.get_budget("2026-11", "FOOD") == 5000


def test_get_budget_not_found(temporary_budget_file):
    assert bs.get_budget("2026-11", "Travel") is None


def test_invalid_month(temporary_budget_file):
    with pytest.raises(ValueError):
        bs.set_budget("2026-13", "Food", "5000")


def test_negative_budget(temporary_budget_file):
    with pytest.raises(ValueError):
        bs.set_budget("2026-11", "Food", "-100")


def test_zero_budget(temporary_budget_file):
    with pytest.raises(ValueError):
        bs.set_budget("2026-11", "Food", "0")


def test_empty_category(temporary_budget_file):
    with pytest.raises(ValueError):
        bs.set_budget("2026-11", "", "5000")


def test_update_nonexistent_budget(temporary_budget_file):
    with pytest.raises(ValueError):
        bs.update_budget("2026-11", "Food", "6000")


def test_delete_budget(temporary_budget_file):
    bs.set_budget("2026-11", "Food", "5000")

    assert bs.delete_budget("2026-11", "Food") is True
    assert bs.get_budget("2026-11", "Food") is None


def test_persistence(temporary_budget_file):
    bs.set_budget("2026-11", "Food", "5000")

    with open(temporary_budget_file, encoding="utf-8") as file:
        data = json.load(file)

    assert data[0]["amount"] == "5000.00"
