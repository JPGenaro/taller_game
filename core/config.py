import customtkinter as ctk

class ConfigManager:
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