import sqlite3
import json
import os
import datetime

class Database:
    def __init__(self, path=None):
        # por defecto usa el archivo taller.db en la raíz del proyecto
        if path:
            self.db_path = path
        else:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.db_path = os.path.join(repo_root, "taller.db")
        self._ensure_schema()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                slot INTEGER PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """)
            conn.commit()

    def hay_partidas_guardadas(self) -> bool:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(1) FROM partidas")
            cnt = cur.fetchone()[0]
            return cnt > 0

    def guardar_partida(self, slot: int, motor):
        """
        Guarda el estado del 'motor' en el slot indicado (reemplaza si existe).
        Se espera que 'motor' tenga método to_dict().
        """
        if not hasattr(motor, "to_dict"):
            raise ValueError("El objeto motor no es serializable (falta to_dict).")
        data = motor.to_dict()
        texto = json.dumps(data, ensure_ascii=False)
        updated = datetime.datetime.utcnow().isoformat()
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("REPLACE INTO partidas(slot, data, updated_at) VALUES (?, ?, ?)", (slot, texto, updated))
            conn.commit()
        return True

    # Alias por si el código usa otro nombre
    guardar = guardar_partida

    def cargar_partida(self, slot: int):
        """Devuelve el dict guardado en el slot o None si no existe."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT data FROM partidas WHERE slot = ?", (slot,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                return json.loads(row[0])
            except Exception:
                return None

    def obtener_resumen_partida(self, slot: int):
        """
        Devuelve un resumen para listar en el menú:
        {"slot": int, "personaje": str, "taller": str, "nivel": int, "updated_at": str}
        o None si no existe.
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT slot, data, updated_at FROM partidas WHERE slot = ?", (slot,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                data = json.loads(row[1])
            except Exception:
                data = {}
            return {
                "slot": row[0],
                "personaje": data.get("personaje", "VACÍO"),
                "taller": data.get("taller", ""),
                "nivel": data.get("nivel", 1),
                "updated_at": row[2]
            }

    def set_config(self, key: str, value: str):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("REPLACE INTO config(key, value) VALUES (?, ?)", (key, value))
            conn.commit()

    def get_config(self, key: str, default: str | None = None):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM config WHERE key = ?", (key,))
            row = cur.fetchone()
            if not row:
                return default
            return row[0]

    def obtener_partida(self, slot: int):
        """
        Compatibilidad con la interfaz antigua.
        Devuelve una tupla (slot, updated_at, personaje, taller, nivel) o None.
        main.py espera que datos[2] sea el nombre (personaje) y datos[4] el nivel.
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT slot, data, updated_at FROM partidas WHERE slot = ?", (slot,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                data = json.loads(row[1])
            except Exception:
                data = {}
            personaje = data.get("personaje", "VACÍO")
            taller = data.get("taller", "")
            nivel = data.get("nivel", 1)
            return (row[0], row[2], personaje, taller, nivel)