from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == order.customer_id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=400, detail="Customer does not exist")

    # create order
    db_order = models.Order(customer_id=order.customer_id, status=order.status)
    db.add(db_order)
    db.flush()  # Flush to get the order ID

    total_amount = 0.0

    # add items to order
    for item in order.items:
        product = (
            db.query(models.Product)
            .filter(models.Product.id == item.product_id)
            .first()
        )
        if not product:
            db.rollback()
            raise HTTPException(
                status_code=404, detail=f"Product ID {item.product_id} does not exist"
            )

        if product.stock < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product ID {item.product_id}. Available: {product.stock}, Requested: {item.quantity}",
            )

        # create order item
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_time=product.price,
        )
        db.add(order_item)

        # update product stock
        product.stock -= item.quantity

        # calculate total amount
        total_amount += item.quantity * product.price

    # update order total amount
    db_order.total_amount = total_amount

    db.commit()
    db.refresh(db_order)
    return db_order
