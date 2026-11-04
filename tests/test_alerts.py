
import pytest

from spendsense.alert_service import (
    calculate_utilization,
    check_budget_thresholds
)


def test_below_80_percent():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 1000, 3000, 5000
    )

    assert alerts == []


def test_cross_80_percent():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 3500, 4000, 5000
    )

    assert len(alerts) == 1
    assert alerts[0]["threshold"] == 80


def test_cross_100_percent():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 4500, 5000, 5000
    )

    assert len(alerts) == 1
    assert alerts[0]["threshold"] == 100


def test_cross_both_thresholds():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 3500, 5500, 5000
    )

    assert len(alerts) == 2
    assert [alert["threshold"] for alert in alerts] == [80, 100]


def test_no_duplicate_80_percent_alert():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 4100, 4200, 5000
    )

    assert alerts == []


def test_zero_budget():
    alerts = check_budget_thresholds(
        "2026-11", "Food", 0, 1000, 0
    )

    assert alerts == []


def test_negative_spending():
    with pytest.raises(ValueError):
        check_budget_thresholds(
            "2026-11", "Food", -100, 100, 5000
        )


def test_updated_spending_lower_than_previous():
    with pytest.raises(ValueError):
        check_budget_thresholds(
            "2026-11", "Food", 3000, 2000, 5000
        )


def test_utilization():
    assert calculate_utilization(4000, 5000) == 80


def test_utilization_above_budget():
    assert calculate_utilization(6000, 5000) == 120
