import customtkinter as ctk

class MenuPausa(ctk.CTkFrame):
    def __init__(self, master, juego):
        # Le ponemos un color un poco distinto para que resalte del fondo
        super().__init__(master, corner_radius=15, border_width=2, border_color="gray")
        self.juego = juego
        # Lo ponemos en el centro sin borrar el taller
        self.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self, text="PAUSA", font=("Arial", 24, "bold")).pack(pady=20, padx=60)

        ctk.CTkButton(self, text="REANUDAR", width=180,
                      command=self.juego.mostrar_taller).pack(pady=10)
        
        ctk.CTkButton(self, text="GUARDAR", fg_color="#2ecc71", width=180,
                      command=self.guardar_y_continuar).pack(pady=10)
        
        ctk.CTkButton(self, text="OPCIONES", width=180,
                      command=self.juego.mostrar_opciones_desde_pausa).pack(pady=10)
        
        ctk.CTkButton(self, text="SALIR AL MENÚ", fg_color="#e74c3c", width=180,
                      command=self.juego.mostrar_menu_inicio).pack(pady=10, padx=20)

    def guardar_y_continuar(self):
        self.juego.db.guardar(self.juego.slot_actual, self.juego.motor)
        # Podrías agregar un pequeño label que diga "Guardado!"