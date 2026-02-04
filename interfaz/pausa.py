import customtkinter as ctk

class MenuPausa(ctk.CTkFrame):
    def __init__(self, master, juego):
        # Color de borde para que resalte
        super().__init__(master, corner_radius=15, border_width=2, border_color="#3498db")
        self.juego = juego
        # 'place' lo pone encima de todo sin borrar el taller
        self.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self, text="PAUSA", font=("Arial", 24, "bold")).pack(pady=20, padx=60)

        # Botones del menú de pausa
        ctk.CTkButton(self, text="REANUDAR", command=self.destroy).pack(pady=10)
        
        ctk.CTkButton(self, text="GUARDAR", fg_color="#2ecc71", 
                      command=self.guardar_partida).pack(pady=10)
        
        ctk.CTkButton(self, text="OPCIONES", 
                      command=self.ir_a_opciones).pack(pady=10)
        
        ctk.CTkButton(self, text="SALIR AL MENÚ", fg_color="#e74c3c", 
                      command=self.juego.mostrar_menu_inicio).pack(pady=10, padx=20)

    def guardar_partida(self):
        self.juego.db.guardar(self.juego.slot_actual, self.juego.motor)
        print("¡Guardado desde el menú de pausa!")

    def ir_a_opciones(self):
        self.juego.limpiar_pantalla()
        # Al volver de opciones, queremos que vuelva a abrir la PAUSA
        from interfaz.opciones import VentanaOpciones
        VentanaOpciones(self.juego.root, al_volver=self.juego.abrir_pausa)