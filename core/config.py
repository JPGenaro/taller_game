import customtkinter as ctk
import os

class ConfigManager:
    @staticmethod
    def project_root() -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    @staticmethod
    def data_path(filename: str) -> str:
        return os.path.join(ConfigManager.project_root(), "datos", filename)

    @staticmethod
    def cambiar_tema(nuevo_tema):
        # nuevo_tema puede ser "dark" o "light"
        ctk.set_appearance_mode(nuevo_tema)
    
    @staticmethod
    def toggle_pantalla_completa(ventana, modo_full):
        if modo_full:
            ventana.attributes("-fullscreen", True)
        else:
            ventana.attributes("-fullscreen", False)

# Game balance defaults (can be overridden and persisted at runtime)
DEFAULTS = {
    "EXP_PER_POINT_DIVISOR": 2,      # puntos_reparados / EXP_PER_POINT_DIVISOR -> EXP gained
    "LEVEL_SELL_MULTIPLIER": 0.20,   # extra multiplier per level (20% per level above 1)
    "REPAIR_COST_PER_POINT": 2,      # costo por punto de reparación
    "REPAIR_COST_CAP_MULTIPLIER": 1.2 # tope respecto al precio de compra (1.2 = 120%)
}

# Year-related pricing defaults
DEFAULTS.update({
    "YEAR_DEPRECIATION": 0.02,   # pérdida de valor por año (por defecto 2% por año)
    "YEAR_MIN_FACTOR": 0.6       # factor mínimo de degradación (no bajar de 0.6)
})

# Initialize module-level constants from defaults so other modules can import them
EXP_PER_POINT_DIVISOR = DEFAULTS["EXP_PER_POINT_DIVISOR"]
LEVEL_SELL_MULTIPLIER = DEFAULTS["LEVEL_SELL_MULTIPLIER"]
REPAIR_COST_PER_POINT = DEFAULTS["REPAIR_COST_PER_POINT"]
REPAIR_COST_CAP_MULTIPLIER = DEFAULTS["REPAIR_COST_CAP_MULTIPLIER"]

def apply_runtime_override(key: str, value):
    """Apply a runtime override to the module constant and return the applied value.
    Key should be one of DEFAULTS keys.
    """
    global EXP_PER_POINT_DIVISOR, LEVEL_SELL_MULTIPLIER, REPAIR_COST_PER_POINT, REPAIR_COST_CAP_MULTIPLIER
    if key not in DEFAULTS:
        raise KeyError(f"Unknown config key: {key}")
    # coerce types based on default type
    default = DEFAULTS[key]
    if isinstance(default, int):
        v = int(value)
    else:
        v = float(value)
    if key == "EXP_PER_POINT_DIVISOR":
        EXP_PER_POINT_DIVISOR = v
    elif key == "LEVEL_SELL_MULTIPLIER":
        LEVEL_SELL_MULTIPLIER = v
    elif key == "REPAIR_COST_PER_POINT":
        REPAIR_COST_PER_POINT = v
    elif key == "REPAIR_COST_CAP_MULTIPLIER":
        REPAIR_COST_CAP_MULTIPLIER = v
    elif key == "YEAR_DEPRECIATION":
        YEAR_DEPRECIATION = v
    elif key == "YEAR_MIN_FACTOR":
        YEAR_MIN_FACTOR = v
    return v

def get_default(key: str):
    return DEFAULTS.get(key)