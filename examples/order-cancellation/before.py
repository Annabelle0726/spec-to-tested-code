"""Deliberately incomplete starting point for the documented exercise."""

from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    owner_id: str
    status: str


def cancel_order(order: Order, actor_id: str) -> bool:
    return True
