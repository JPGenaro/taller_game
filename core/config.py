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