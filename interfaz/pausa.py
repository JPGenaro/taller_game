import customtkinter as ctk
from core.ui_theme import COLORS, FONTS

class MenuPausa(ctk.CTkFrame):
    def __init__(self, master, juego):
        # Frame con borde y esquinas redondeadas para que resalte
        super().__init__(master, corner_radius=15, border_width=2, border_color=COLORS["accent"], fg_color=COLORS["panel"])
        self.juego = juego
        
        # 'place' lo ubica en el centro exacto de la ventana principal
        self.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self, text="PAUSA", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=20, padx=60)

        # --- BOTONES DEL MENÚ ---
        
        # REANUDAR: Simplemente destruye este frame de pausa
        ctk.CTkButton(self, text="REANUDAR", width=200, height=35,
                  fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.destroy).pack(pady=10)
        
        # GUARDAR: Llama a la base de datos usando el slot actual
        ctk.CTkButton(self, text="GUARDAR PARTIDA", width=200, height=35, fg_color=COLORS["accent_2"], 
                      command=self.guardar_y_continuar).pack(pady=10)
        
        # OPCIONES: Limpia todo y va a la pantalla de opciones
        ctk.CTkButton(self, text="OPCIONES", width=200, height=35,
                  fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.ir_a_opciones).pack(pady=10)
        
        # SALIR: Vuelve al menú principal (el método de Aplicacion limpia la pantalla)
        ctk.CTkButton(self, text="SALIR AL MENÚ", width=200, height=35, fg_color=COLORS["danger"], 
                      command=self.juego.mostrar_menu_inicio).pack(pady=10, padx=20)

    def guardar_y_continuar(self):
        """Usa la instancia del juego para guardar el estado actual."""
        self.juego.guardar_partida(self.juego.slot_actual, parent_window=self)

    def ir_a_opciones(self):
        """Navega a la pantalla de opciones."""
        self.juego.limpiar_pantalla()
        from interfaz.opciones import VentanaOpciones
        # Al volver de opciones, queremos que abra el menú de pausa de nuevo
        VentanaOpciones(self.juego.root, al_volver=self.juego.abrir_pausa, db=self.juego.db)