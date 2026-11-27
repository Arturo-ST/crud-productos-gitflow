"""Validación de los datos ingresados por el usuario."""
import math

def validate_product(data):
    if not isinstance(data, dict):
        raise ValueError("Datos inválidos")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "")
    precio = data.get("precio")
    cantidad = data.get("cantidad")
    if not isinstance(nombre, str) or not 1 <= len(nombre.strip()) <= 100:
        raise ValueError("El nombre debe contener entre 1 y 100 caracteres")
    if not isinstance(descripcion, str) or len(descripcion) > 500:
        raise ValueError("La descripción debe contener máximo 500 caracteres")
    if isinstance(precio, bool) or not isinstance(precio, (float, int)) or not math.isfinite(precio) or precio < 0:
        raise ValueError("El precio debe ser un número no negativo")
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
        raise ValueError("La cantidad debe ser un entero no negativo")
    return {"nombre": nombre.strip(), "descripcion": descripcion.strip(),
            "precio": round(precio, 2), "cantidad": cantidad}
