import sqlite3

class Database:
    def __init__(self):
        self.db_name = "taller.db"
        self.setup()

    def setup(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Agregamos 'slot_id' como clave primaria
            cursor.execute('''CREATE TABLE IF NOT EXISTS partidas (
                slot_id INTEGER PRIMARY KEY,
                personaje TEXT,
                taller TEXT,
                dinero INTEGER,
                nivel INTEGER,
                exp INTEGER
            )''')
            conn.commit()

    def obtener_partida(self, slot_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM partidas WHERE slot_id = ?", (slot_id,))
            return cursor.fetchone()

    def guardar(self, slot_id, motor):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT OR REPLACE INTO partidas 
                              (slot_id, personaje, taller, dinero, nivel, exp) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (slot_id, motor.personaje, motor.taller, motor.dinero, motor.nivel, motor.exp))
            conn.commit()