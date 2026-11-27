"""Registro de productos."""
from app import connection

def handle(data):
    from features.validate import validate_product
    clean = validate_product(data)
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (?, ?, ?, ?)",
            (clean["nombre"], clean["descripcion"], clean["precio"], clean["cantidad"]))
        new_id = cursor.lastrowid
    return 201, {"id": new_id, **clean}
