from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

from .routes import customer_router, order_router, product_router

# create FastAPI app
app = FastAPI(
    description="A FastAPI application using MCP",
    title="My FastAPI Application",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers for products, customers, and orders
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(order_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI application using MCP!",
        "endpoints": {
            "products": "/products",
            "customers": "/customers",
            "orders": "/orders",
            "docs": "/docs",
        },
    }


mcp = FastApiMCP(app)
mcp.mount()
