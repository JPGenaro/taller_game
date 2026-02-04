import customtkinter as ctk

class MenuPausa(ctk.CTkFrame):
    def __init__(self, master, juego):
        super().__init__(master, corner_radius=15, border_width=2)
        self.juego = juego
        self.place(relx=0.5, rely=0.5, anchor="center") # Lo centramos perfecto

        ctk.CTkLabel(self, text="PAUSA", font=("Arial", 24, "bold")).pack(pady=20, padx=50)

        # --- BOTONES ---
        ctk.CTkButton(self, text="REANUDAR", command=self.juego.mostrar_taller).pack(pady=10)
        
        ctk.CTkButton(self, text="GUARDAR", fg_color="#2ecc71", 
                      command=self.guardar_y_continuar).pack(pady=10)
        
        ctk.CTkButton(self, text="OPCIONES", 
                      command=self.juego.mostrar_opciones_desde_pausa).pack(pady=10)
        
        ctk.CTkButton(self, text="SALIR AL MENÚ", fg_color="#e74c3c", 
                      command=self.juego.mostrar_menu_inicio).pack(pady=10)

    def guardar_y_continuar(self):
        self.juego.db.guardar(self.juego.slot_actual, self.juego.motor)
        print("Partida guardada con éxito")