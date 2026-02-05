import customtkinter as ctk

class MenuPausa(ctk.CTkFrame):
    def __init__(self, master, juego):
        # Frame con borde para que resalte
        super().__init__(master, corner_radius=15, border_width=2, border_color="#3b8ed0")
        self.juego = juego
        
        # 'place' lo ubica en el centro exacto sin matar lo que hay de fondo
        self.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self, text="PAUSA", font=("Arial", 25, "bold")).pack(pady=20, padx=60)

        # BOTONES
        ctk.CTkButton(self, text="REANUDAR", width=200, 
                      command=self.destroy).pack(pady=10)
        
        ctk.CTkButton(self, text="GUARDAR", width=200, fg_color="#2ecc71", 
                      command=self.guardar_partida).pack(pady=10)
        
        ctk.CTkButton(self, text="OPCIONES", width=200,
                      command=self.ir_a_opciones).pack(pady=10)
        
        ctk.CTkButton(self, text="SALIR AL MENÚ", width=200, fg_color="#e74c3c", 
                      command=self.juego.mostrar_menu_inicio).pack(pady=10, padx=20)

    def guardar_partida(self):
        self.juego.db.guardar(self.juego.slot_actual, self.juego.motor)
        print("Guardado exitoso.")

    def ir_a_opciones(self):
        self.juego.limpiar_pantalla()
        # Al volver de opciones, queremos que abra la pausa de nuevo
        from interfaz.opciones import VentanaOpciones
        VentanaOpciones(self.juego.root, al_volver=self.juego.abrir_pausa)