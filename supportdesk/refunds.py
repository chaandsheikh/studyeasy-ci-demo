"""Refunds for SupportDesk orders."""


def refund_amount(order_total, percent):
    """the refund for a partial refund of an order, in the order's currency"""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(order_total * percent / 100, 2)
