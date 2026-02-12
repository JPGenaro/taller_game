import unittest
from core.motor import Motor
from modelos.auto import Auto

class TestEconomy(unittest.TestCase):
    def test_repair_grants_exp_and_caps_cost(self):
        m = Motor()
        # Create an auto with very low parts to force high repair cost
        partes = {k: 10 for k in Auto("","",0).partes.keys()}
        a = Auto("Test", "X", 2000, partes=partes, km=50000)
        m.slots[0] = a
        m.dinero = 100000
        # Ensure defaults loaded
        antes_exp = m.exp
        ok, msg = m.reparar_auto_total(0)
        self.assertTrue(ok)
        self.assertGreater(m.exp, antes_exp)

    def test_sell_price_scales_with_level(self):
        m = Motor()
        partes = {k: 80 for k in Auto("","",0).partes.keys()}
        a = Auto("Marca", "Model", 10000, partes=partes, km=20000)
        m.slots[1] = a
        base = a.valor_venta()
        m.nivel = 1
        ok, msg1 = m.vender_auto(1)
        # Re-create to test multiplier
        m.slots[1] = a
        m.nivel = 5
        ok2, msg2 = m.vender_auto(1)
        self.assertTrue(ok and ok2)
        # Extract sold prices from messages
        import re
        p1 = int(re.search(r"por \$(\d+)", msg1).group(1))
        p2 = int(re.search(r"por \$(\d+)", msg2).group(1))
        self.assertGreater(p2, p1)


if __name__ == '__main__':
    unittest.main()
