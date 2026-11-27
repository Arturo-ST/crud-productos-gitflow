"""Consulta de productos."""
from app import connection

def handle():
    with connection() as db:
        products = db.execute(
            "SELECT id, nombre, descripcion, precio, cantidad FROM productos ORDER BY id DESC"
        ).fetchall()
    return 200, {"productos": [dict(p) for p in products]}
