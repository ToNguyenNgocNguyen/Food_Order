from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    """
    Represents an item in an order with its details.
    """

    # order_id: str = Field(..., description="Unique identifier for the order.")
    item_id: int = Field(..., description="Unique identifier for the item.")
    quantity: float = Field(..., description="Quantity of the item ordered.")
    total_price: float = Field(..., description="Total price for the item.")

class Items(BaseModel):
    """
    Represents a collection of items in an order.
    """

    items: List[Item] = Field(..., description="List of items in the order.")
