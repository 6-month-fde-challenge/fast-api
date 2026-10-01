"""Product and order endpoints."""
from fastapi import APIRouter

from app.schemas import Order, OrderCreate, Product, ProductCreate, StatusUpdate
from app.service import OrderService, ProductService

router = APIRouter()
product_service = ProductService()
order_service = OrderService(product_service)     # orders read from the same catalogue

# Error responses listed here also show up in Swagger UI next to each endpoint.
NOT_FOUND = {404: {"description": "Product or order not found"}}
BAD_ORDER = {400: {"description": "Not enough stock"}}
BAD_STATUS = {400: {"description": "Status change not allowed (must go one step forward)"}}


# ---------- products ----------
@router.post("/products", response_model=Product, status_code=201, tags=["Products"])
def create_product(product: ProductCreate):
    return product_service.create(product)


@router.get("/products", response_model=list[Product], tags=["Products"])
def get_products():
    return product_service.list_all()


# ---------- orders ----------
@router.post("/orders", response_model=Order, status_code=201, tags=["Orders"],
             responses={**NOT_FOUND, **BAD_ORDER})
def place_order(order: OrderCreate):
    return order_service.place(order)


@router.get("/orders", response_model=list[Order], tags=["Orders"])
def get_orders():
    return order_service.list_all()


@router.get("/orders/{order_id}", response_model=Order, tags=["Orders"], responses=NOT_FOUND)
def get_order(order_id: int):
    return order_service.get(order_id)


@router.put("/orders/{order_id}/status", response_model=Order, tags=["Orders"],
            responses={**NOT_FOUND, **BAD_STATUS})
def update_order_status(order_id: int, update: StatusUpdate):
    return order_service.change_status(order_id, update.status)
