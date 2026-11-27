"""Eliminación de productos."""
from app import connection

def handle(item_id):
    with connection() as db:
        result = db.execute("DELETE FROM productos WHERE id=?", (item_id,))
        if result.rowcount == 0:
            return 404, {"error": "Producto no encontrado"}
    return 200, {"mensaje": "Producto eliminado", "id": item_id}
