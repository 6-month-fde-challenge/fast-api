"""Pydantic models for products and orders."""
import re
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderStatus(str, Enum):
    """The only four statuses an order can have, in the order they happen."""
    PLACED = "PLACED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


# ---------- products ----------
class ProductCreate(BaseModel):
    # strip spaces at both ends before any rule is checked
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100, examples=["Wireless Mouse"])
    price: float = Field(gt=0, le=1_000_000, examples=[799.0])
    stock: int = Field(ge=0, le=100_000, examples=[25])

    @field_validator("name")
    @classmethod
    def name_has_letters(cls, value):
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("product name must contain at least one letter")
        return " ".join(value.split())               # "Wireless    Mouse" -> "Wireless Mouse"

    @field_validator("price")
    @classmethod
    def price_two_decimals(cls, value):
        # money has paise, not fractions of paise: 799.99 is fine, 799.999 is not
        if round(value, 2) != value:
            raise ValueError("price may have at most 2 decimal places")
        return value


class Product(ProductCreate):
    id: int


# ---------- orders: what the client sends ----------
class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0, examples=[1])
    quantity: int = Field(gt=0, le=100, examples=[2])


class OrderCreate(BaseModel):
    # extra="forbid" rejects any field not listed here. So a client that tries
    # to send its own "total_amount" or "status" gets a 422 error.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer: str = Field(min_length=2, max_length=50, examples=["Aarav"])
    items: list[OrderItemCreate] = Field(min_length=1, max_length=20)

    @field_validator("customer")
    @classmethod
    def customer_is_a_name(cls, value):
        if not re.fullmatch(r"[A-Za-z .'-]+", value):
            raise ValueError("customer may contain only letters, spaces, dots, hyphens and apostrophes")
        return " ".join(value.split()).title()        # "aarav  sharma" -> "Aarav Sharma"

    @field_validator("items")
    @classmethod
    def no_duplicate_products(cls, items):
        ids = [item.product_id for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError("each product may appear only once - increase its quantity instead")
        return items


# ---------- orders: what the server sends back ----------
class OrderItem(BaseModel):
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    line_total: float


class Order(BaseModel):
    id: int
    customer: str
    items: list[OrderItem]
    total_amount: float
    status: OrderStatus


class StatusUpdate(BaseModel):
    status: OrderStatus = Field(examples=["PROCESSING"])
