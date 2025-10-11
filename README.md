# mcp-example
FastAPI API with a MCP Server

## Overview
A FastAPI application with full CRUD REST APIs for products, customers, and orders. Uses SQLite3 for local development.

## Features
- **Products API**: Full CRUD operations for managing products
- **Customers API**: Full CRUD operations for managing customers
- **Orders API**: Full CRUD operations for managing orders with order items
- **SQLite Database**: Local SQLite3 database for development
- **Automatic Documentation**: Interactive API docs at `/docs` and `/redoc`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Products
- `POST /products/` - Create a new product
- `GET /products/` - Get all products (with pagination)
- `GET /products/{product_id}` - Get a specific product
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - Get all customers (with pagination)
- `GET /customers/{customer_id}` - Get a specific customer
- `PUT /customers/{customer_id}` - Update a customer
- `DELETE /customers/{customer_id}` - Delete a customer

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/` - Get all orders (with pagination)
- `GET /orders/{order_id}` - Get a specific order
- `GET /customers/{customer_id}/orders` - Get all orders for a customer
- `PUT /orders/{order_id}` - Update an order (status)
- `DELETE /orders/{order_id}` - Delete an order

## Example Usage

### Create a Product
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock": 50
  }'
```

### Create a Customer
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "address": "123 Main St"
  }'
```

### Create an Order
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "status": "pending",
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

## Database

The application uses SQLite3 with the database file `app.db` stored in the project root. The database is automatically created when you first run the application.

### Database Schema

**Products Table**
- id (Primary Key)
- name
- description
- price
- stock
- created_at
- updated_at

**Customers Table**
- id (Primary Key)
- name
- email (Unique)
- phone
- address
- created_at
- updated_at

**Orders Table**
- id (Primary Key)
- customer_id (Foreign Key)
- order_date
- status
- total_amount
- created_at
- updated_at

**Order Items Table**
- id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- price

## License

GPL-3.0

