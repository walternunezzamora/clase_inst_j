from fastapi import FastAPI
from .database import Base, engine
from .routers import productos, clientes, ventas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Tienda")

app.include_router(productos.router)
app.include_router(clientes.router)
app.include_router(ventas.router)
