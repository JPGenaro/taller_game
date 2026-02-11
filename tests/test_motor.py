import unittest
from core.motor import Motor
from modelos.auto import Auto


class TestMotor(unittest.TestCase):
    def test_to_dict_and_from_dict_roundtrip(self):
        motor = Motor()
        motor.personaje = "Ana"
        motor.taller = "Taller Azul"
        motor.dinero = 1234
        motor.nivel = 3
        motor.exp = 45
        motor.slots = [Auto("Fiat", "Uno", 1000), None, Auto("Ford", "Falcon", 2000)]

        data = motor.to_dict()
        rebuilt = Motor.from_dict(data)

        self.assertEqual(rebuilt.personaje, motor.personaje)
        self.assertEqual(rebuilt.taller, motor.taller)
        self.assertEqual(rebuilt.dinero, motor.dinero)
        self.assertEqual(rebuilt.nivel, motor.nivel)
        self.assertEqual(rebuilt.exp, motor.exp)
        self.assertEqual(rebuilt.slots[0].marca, motor.slots[0].marca)
        self.assertIsNone(rebuilt.slots[1])
        self.assertEqual(rebuilt.slots[2].modelo, motor.slots[2].modelo)


if __name__ == "__main__":
    unittest.main()
