"""Refunds for SupportDesk orders."""
import logging

log = logging.getLogger("supportdesk.refunds")


def refund_amount(order_total, percent):
    """the refund for a partial refund of an order, in the order's currency"""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(order_total * percent / 100, 2)


def goodwill_refund(order_total, percent, bonus, customer):
    """a partial refund plus a goodwill bonus for a late order"""
    amount = min(refund_amount(order_total, percent) + bonus, order_total)
    log.info("goodwill refund %s to %s", amount, customer["id"])
    return amount


REASONS = {"late": "Order arrived late", "damaged": "Item arrived damaged",
           "wrong_item": "Wrong item sent"}


def refund_reason(code):
    """the text shown to the customer for a refund reason code"""
    if code not in REASONS:
        raise ValueError(f"unknown refund reason: {code}")
    return REASONS[code]
