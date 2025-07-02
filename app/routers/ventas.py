from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Venta)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # Verificar existencia del cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == venta.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Crear la venta
    db_venta = models.Venta(cliente_id=venta.cliente_id)
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    # Crear detalles de venta
    for detalle in venta.detalles:
        producto = db.query(models.Producto).filter(models.Producto.id == detalle.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} no encontrado")

        if producto.stock < detalle.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto {producto.nombre}")

        subtotal = producto.precio * detalle.cantidad
        detalle_venta = models.DetalleVenta(
            venta_id=db_venta.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            subtotal=subtotal
        )
        producto.stock -= detalle.cantidad
        db.add(detalle_venta)

    db.commit()
    db.refresh(db_venta)
    return db_venta

@router.get("/", response_model=list[schemas.Venta])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()
