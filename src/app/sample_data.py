"""
Script to generate sample data for testing the API.
To run this script, execute:
    python src/app/sample_data.py
"""

from sqlalchemy.orm.session import Session

from app import models
from app.database import SessionLocal


def create_sample_data() -> None:
    print("TEST: Creating sample data...")
    db: Session = SessionLocal()

    if db.query(models.Product).count() > 0:
        print("Sample data already exists. Skipping creation.")
        db.close()
        return

    try:
        # create sample customers
        customer_list = [
            models.Customer(
                name="Alice",
                email="alice@example.com",
                phone="123-456-7890",
                address="123 Main St, Anytown, USA",
            ),
            models.Customer(
                name="Bob",
                email="bob@example.com",
                phone="987-654-3210",
                address="456 Elm St, Othertown, USA",
            ),
            models.Customer(
                name="Charlie",
                email="charlie@example.com",
                phone="555-555-5555",
                address="789 Oak St, Sometown, USA",
            ),
            models.Customer(
                name="Diana",
                email="diana@example.com",
                phone="444-444-4444",
                address="321 Pine St, Anycity, USA",
            ),
        ]
        db.add_all(customer_list)
        db.commit()
        print(f"Created {len(customer_list)} customers.")

        # create sample products
        product_list = [
            models.Product(
                name="Widget A", description="A basic widget", price=9.99, stock=100
            ),
            models.Product(
                name="Widget B",
                description="A more advanced widget",
                price=19.99,
                stock=50,
            ),
            models.Product(
                name="Gadget X",
                description="An innovative gadget",
                price=29.99,
                stock=75,
            ),
            models.Product(
                name="Gadget Y", description="A premium gadget", price=49.99, stock=30
            ),
            models.Product(
                name="Thingamajig",
                description="A useful thingamajig",
                price=14.99,
                stock=200,
            ),
        ]
        db.add_all(product_list)
        db.commit()
        print(f"Created {len(product_list)} products.")

        # refresh customers and products to get their IDs
        products = db.query(models.Product).all()
        customers = db.query(models.Customer).all()

        # create sample orders
        # order 1 for Alice
        order1 = models.Order(customer_id=customers[0].id, status="completed")
        db.add(order1)
        db.commit()
        db.refresh(order1)
        item1_1 = models.OrderItem(
            order_id=order1.id,
            product_id=products[0].id,
            quantity=2,
            price_at_time=products[0].price,
        )
        item1_2 = models.OrderItem(
            order_id=order1.id,
            product_id=products[2].id,
            quantity=1,
            price_at_time=products[2].price,
        )
        db.add_all([item1_1, item1_2])

        # update order1 total_amount
        order1.total_amount = (
            item1_1.quantity * item1_1.price_at_time
            + item1_2.quantity * item1_2.price_at_time
        )
        db.commit()
        print("Created order 1 for Alice.")

        # order 2 for Bob
        order2 = models.Order(customer_id=customers[1].id, status="pending")
        db.add(order2)
        db.commit()
        db.refresh(order2)
        item2_1 = models.OrderItem(
            order_id=order2.id,
            product_id=products[1].id,
            quantity=1,
            price_at_time=products[1].price,
        )
        db.add(item2_1)
        order2.total_amount = item2_1.quantity * item2_1.price_at_time
        db.commit()
        print("Created order 2 for Bob.")

    except Exception as err:
        db.rollback()
        print(f"Error occurred: {err}")
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
