"""Modificación de productos."""
from app import connection

def handle(item_id, data):
    from features.validate import validate_product
    clean = validate_product(data)
    with connection() as db:
        result = db.execute(
            "UPDATE productos SET nombre=?, descripcion=?, precio=?, cantidad=? WHERE id=?",
            (clean["nombre"], clean["descripcion"], clean["precio"], clean["cantidad"], item_id))
        if result.rowcount == 0:
            return 404, {"error": "Producto no encontrado"}
    return 200, {"id": item_id, **clean}
