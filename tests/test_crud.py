"""Pruebas unitarias para las funciones CRUD (ejecutar con python -m unittest discover -s tests)."""
import tempfile
from pathlib import Path
import unittest
import app
from features import create, read, update, delete, validate

class CrudTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app.DB_PATH = Path(self.temp.name) / "test.db"
        app.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_flow(self):
        status, item = create.handle({"nombre":"Mouse","descripcion":"Inalámbrico","precio":400,"cantidad":2})
        self.assertEqual(status,201)
        self.assertEqual(len(read.handle()[1]["productos"]),1)
        status, updated = update.handle(item["id"],{"nombre":"Mouse nuevo","precio":450.5,"cantidad":3})
        self.assertEqual(status,200)
        self.assertEqual(updated["nombre"],"Mouse nuevo")
        self.assertEqual(delete.handle(item["id"])[0],200)
        self.assertEqual(read.handle()[1]["productos"],[])
        self.assertEqual(delete.handle(item["id"])[0],404)

    def test_validation(self):
        for bad in [
            {"nombre":"","precio":5,"cantidad":2},
            {"nombre":"T","precio":-3,"cantidad":2},
            {"nombre":"T","precio":3,"cantidad":1.5},
            {"nombre":"T","precio":True,"cantidad":2},
        ]:
            with self.assertRaises(ValueError):
                validate.validate_product(bad)

if __name__ == "__main__":
    unittest.main()
