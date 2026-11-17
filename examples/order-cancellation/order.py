"""In-memory order cancellation exercise."""

from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    owner_id: str
    status: str


def cancel_order(order: Order, actor_id: str) -> bool:
    if actor_id != order.owner_id or order.status != "unshipped":
        return False
    order.status = "cancelled"
    return True
