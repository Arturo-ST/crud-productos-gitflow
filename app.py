"""Servidor HTTP del CRUD de productos sin dependencias externas."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import mimetypes
import sqlite3
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
DB_PATH = ROOT / "productos.db"

def connection():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def initialize():
    with connection() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL DEFAULT '',
            precio REAL NOT NULL CHECK(precio >= 0),
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0)
        )""")

def respond(handler, code, value):
    payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)

def read_json(handler):
    size = int(handler.headers.get("Content-Length", "0"))
    if size > 65536:
        raise ValueError("Solicitud demasiado grande")
    if size <= 0:
        raise ValueError("Debe enviar un JSON")
    try:
        value = json.loads(handler.rfile.read(size))
    except (ValueError, UnicodeDecodeError):
        raise ValueError("JSON inválido")
    if not isinstance(value, dict):
        raise ValueError("Se espera un objeto JSON")
    return value

def dispatch(method, path, data=None):
    """Los módulos se incorporan individualmente desde las ramas feature/."""
    try:
        from features import create, read, update, delete
    except ImportError:
        pass
    else:
        if path == "/api/productos" and method == "POST":
            return create.handle(data)
        if path == "/api/productos" and method == "GET":
            return read.handle()
        if path.startswith("/api/productos/"):
            try:
                item_id = int(path.rsplit("/", 1)[-1])
            except ValueError:
                return 400, {"error": "ID inválido"}
            if item_id < 1:
                return 400, {"error": "ID inválido"}
            if method == "PUT":
                return update.handle(item_id, data)
            if method == "DELETE":
                return delete.handle(item_id)
    return 404, {"error": "Ruta no encontrada"}

class Handler(BaseHTTPRequestHandler):
    def api(self, method):
        path = urlsplit(self.path).path
        try:
            data = read_json(self) if method in ("POST", "PUT") else None
            code, body = dispatch(method, path, data)
        except ValueError as exc:
            code, body = 400, {"error": str(exc)}
        except sqlite3.Error:
            code, body = 500, {"error": "Error de base de datos"}
        respond(self, code, body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path.startswith("/api/"):
            return self.api("GET")
        if path == "/":
            path = "/index.html"
        permitted = {"/index.html", "/style.css", "/script.js"}
        if path not in permitted:
            return respond(self, 404, {"error": "Archivo no encontrado"})
        target = ROOT / "static" / path.lstrip("/")
        if not target.is_file():
            return respond(self, 404, {"error": "Interfaz aún no disponible"})
        raw = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "text/plain")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        self.api("POST")

    def do_PUT(self):
        self.api("PUT")

    def do_DELETE(self):
        self.api("DELETE")

if __name__ == "__main__":
    initialize()
    print("CRUD disponible en http://localhost:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
