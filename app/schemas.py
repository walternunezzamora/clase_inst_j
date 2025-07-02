from pydantic import BaseModel
from datetime import datetime
from typing import List

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    class Config:
        orm_mode = True

class ClienteBase(BaseModel):
    nombre: str
    email: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    class Config:
        orm_mode = True

class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int
    subtotal: float

class DetalleVenta(DetalleVentaBase):
    id: int
    class Config:
        orm_mode = True

class VentaBase(BaseModel):
    cliente_id: int

class VentaCreate(VentaBase):
    detalles: List[DetalleVentaBase]

class Venta(VentaBase):
    id: int
    fecha: datetime
    cliente: Cliente
    detalles: List[DetalleVenta]
    class Config:
        orm_mode = True
