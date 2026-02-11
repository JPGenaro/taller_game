import os
import tempfile
import unittest
from core.database import Database
from core.motor import Motor


class TestDatabase(unittest.TestCase):
    def test_guardar_y_cargar_partida(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_taller.db")
            db = Database(path=db_path)

            motor = Motor()
            motor.personaje = "Luis"
            motor.taller = "Taller Rojo"
            motor.dinero = 500
            motor.nivel = 2
            motor.exp = 10

            db.guardar_partida(1, motor)
            data = db.cargar_partida(1)

            self.assertIsInstance(data, dict)
            self.assertEqual(data.get("personaje"), "Luis")
            self.assertEqual(data.get("taller"), "Taller Rojo")
            self.assertEqual(data.get("dinero"), 500)

    def test_config_persistencia(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_taller.db")
            db = Database(path=db_path)

            db.set_config("tema", "Dark")
            self.assertEqual(db.get_config("tema"), "Dark")
            self.assertEqual(db.get_config("no_existe", "x"), "x")


if __name__ == "__main__":
    unittest.main()
