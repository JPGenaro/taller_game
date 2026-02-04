import sqlite3

class Database:
    def __init__(self):
        self.db_name = "taller.db"
        self.setup()

    def setup(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS partida (
                id INTEGER PRIMARY KEY,
                personaje TEXT,
                taller TEXT,
                dinero INTEGER,
                nivel INTEGER,
                exp INTEGER
            )''')
            conn.commit()

    def guardar(self, motor):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Borramos anterior y guardamos nuevo (simplificado para 1 sola partida)
            cursor.execute("DELETE FROM partida")
            cursor.execute("INSERT INTO partida VALUES (1, ?, ?, ?, ?, ?)",
                           (motor.personaje, motor.taller, motor.dinero, motor.nivel, motor.exp))
            conn.commit()