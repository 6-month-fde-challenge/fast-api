"""Two service classes: one for the product catalogue, one for orders."""
from app.exceptions import InvalidStatusChangeError, NotFoundError, OutOfStockError
from app.schemas import Order, OrderCreate, OrderItem, OrderStatus, Product, ProductCreate

# PLACED -> PROCESSING -> SHIPPED -> DELIVERED, one step at a time
STATUS_FLOW = [OrderStatus.PLACED, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED]


class ProductService:

    def __init__(self):
        self.products = {}
        self.next_id = 1

    def create(self, data: ProductCreate) -> Product:
        product = Product(id=self.next_id, **data.model_dump())
        self.products[product.id] = product
        self.next_id += 1
        return product

    def list_all(self) -> list[Product]:
        return list(self.products.values())

    def get(self, product_id: int) -> Product:
        if product_id not in self.products:
            raise NotFoundError(f"Product {product_id} not found")
        return self.products[product_id]


class OrderService:
    """Places orders. It uses a ProductService to look up prices and stock."""

    def __init__(self, products: ProductService):
        self.products = products
        self.orders = {}
        self.next_id = 1

    def place(self, data: OrderCreate) -> Order:
        # Step 1 - check every item before changing anything
        for item in data.items:
            product = self.products.get(item.product_id)          # 404 if missing
            if item.quantity > product.stock:
                raise OutOfStockError(product.name, product.stock, item.quantity)

        # Step 2 - all items are fine: reduce stock and work out the prices HERE,
        # from our own product list. The client never sends a price or a total.
        order_items = []
        for item in data.items:
            product = self.products.get(item.product_id)
            product.stock -= item.quantity
            order_items.append(OrderItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
                line_total=round(product.price * item.quantity, 2),
            ))
        total = round(sum(i.line_total for i in order_items), 2)

        order = Order(id=self.next_id, customer=data.customer, items=order_items,
                      total_amount=total, status=OrderStatus.PLACED)
        self.orders[order.id] = order
        self.next_id += 1
        return order

    def list_all(self) -> list[Order]:
        return list(self.orders.values())

    def get(self, order_id: int) -> Order:
        if order_id not in self.orders:
            raise NotFoundError(f"Order {order_id} not found")
        return self.orders[order_id]

    def change_status(self, order_id: int, new_status: OrderStatus) -> Order:
        order = self.get(order_id)
        current = STATUS_FLOW.index(order.status)
        if current == len(STATUS_FLOW) - 1:
            raise InvalidStatusChangeError("Order is already DELIVERED - status cannot change")
        allowed = STATUS_FLOW[current + 1]
        if new_status != allowed:
            raise InvalidStatusChangeError(
                f"Cannot move from {order.status.value} to {new_status.value}. "
                f"Next allowed status is {allowed.value}")
        order.status = new_status
        return order
