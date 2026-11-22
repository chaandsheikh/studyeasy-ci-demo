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
