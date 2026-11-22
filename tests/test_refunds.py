import pathlib, sys
import pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "supportdesk"))
from refunds import refund_amount


def test_full_refund(order_total):
    assert refund_amount(order_total, 100) == order_total


def test_half_refund(order_total):
    assert refund_amount(order_total, 50) == 20.0


def test_percent_out_of_range(order_total):
    with pytest.raises(ValueError):
        refund_amount(order_total, 120)


def test_goodwill_refund(order_total):
    from refunds import goodwill_refund
    customer = {"id": "C-12", "email": "c12@example.com"}
    assert goodwill_refund(order_total, 50, 5, customer) == 25.0


def test_goodwill_refund_never_exceeds_the_order(order_total):
    from refunds import goodwill_refund
    customer = {"id": "C-12", "email": "c12@example.com"}
    assert goodwill_refund(order_total, 100, 5, customer) == order_total


def test_refund_reason():
    from refunds import refund_reason
    assert refund_reason("late") == "Order arrived late"
    with pytest.raises(ValueError):
        refund_reason("because")
