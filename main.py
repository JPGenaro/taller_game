import customtkinter as ctk

class JuegoTaller:
    def __init__(self):
        self.ventana_actual = None
        # Sistema de Progreso
        self.datos = {
            "personaje": "",
            "taller": "",
            "dinero": 5000,
            "nivel": 1,
            "exp": 0,
            "exp_sig_nivel": 100
        }
        # Inventario: Slot 0 (Elevador), Slot 1 y 2 (Estacionamiento)
        self.autos_en_taller = [None, None, None] 
        self.mostrar_menu_inicio()

    def limpiar_ventana(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

    # --- (Las funciones de Menu y Perfil se mantienen igual que antes) ---
    def mostrar_menu_inicio(self):
        self.limpiar_ventana()
        self.ventana_actual = ctk.CTk()
        self.ventana_actual.title("Garage Tycoon")
        self.ventana_actual.geometry("900x700")
        self.ventana_actual.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.ventana_actual, text="GARAGE TYCOON", font=("Arial", 40, "bold")).grid(row=0, pady=50)
        ctk.CTkButton(self.ventana_actual, text="JUGAR", command=self.mostrar_creacion_perfil).grid(row=1, pady=10)
        self.ventana_actual.mainloop()

    def mostrar_creacion_perfil(self):
        self.limpiar_ventana()
        self.ventana_actual = ctk.CTk()
        self.ventana_actual.geometry("900x700")
        self.ventana_actual.grid_columnconfigure(0, weight=1)
        
        self.entry_personaje = ctk.CTkEntry(self.ventana_actual, placeholder_text="Nombre del Mecánico", width=300)
        self.entry_personaje.grid(row=1, pady=10)
        self.entry_taller = ctk.CTkEntry(self.ventana_actual, placeholder_text="Nombre del Taller", width=300)
        self.entry_taller.grid(row=2, pady=10)
        
        ctk.CTkButton(self.ventana_actual, text="COMENZAR", command=self.guardar_y_comenzar).grid(row=3, pady=20)
        self.ventana_actual.mainloop()

    def guardar_y_comenzar(self):
        self.datos["personaje"] = self.entry_personaje.get()
        self.datos["taller"] = self.entry_taller.get()
        if self.datos["personaje"] and self.datos["taller"]:
            self.mostrar_taller_principal()

    # --- PANTALLA PRINCIPAL DEL JUEGO ---
    def mostrar_taller_principal(self):
        self.limpiar_ventana()
        self.ventana_actual = ctk.CTk()
        self.ventana_actual.title(f"Gestionando: {self.datos['taller']}")
        self.ventana_actual.geometry("1000x700")

        # 1. BARRA SUPERIOR (Stats)
        header = ctk.CTkFrame(self.ventana_actual, height=80)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text=f"👤 {self.datos['personaje']}", font=("Arial", 16)).pack(side="left", padx=20)
        ctk.CTkLabel(header, text=f"💰 ${self.datos['dinero']}", font=("Arial", 18, "bold"), text_color="#2ecc71").pack(side="left", padx=20)
        
        exp_texto = f"Nivel {self.datos['nivel']} ({self.datos['exp']}/{self.datos['exp_sig_nivel']} EXP)"
        ctk.CTkLabel(header, text=exp_texto).pack(side="right", padx=20)

        # 2. ZONA CENTRAL (Los 3 Slots)
        main_container = ctk.CTkFrame(self.ventana_actual, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        main_container.grid_columnconfigure((0,1,2), weight=1)

        titulos = ["🚧 ELEVADOR (S1)", "🅿️ PARKING (S2)", "🅿️ PARKING (S3)"]
        colores = ["#34495e", "#2c3e50", "#2c3e50"]

        for i in range(3):
            slot_frame = ctk.CTkFrame(main_container, fg_color=colores[i], border_width=2)
            slot_frame.grid(row=0, column=i, padx=10, sticky="nsew")
            
            ctk.CTkLabel(slot_frame, text=titulos[i], font=("Arial", 14, "bold")).pack(pady=10)
            
            # Estado del auto en el slot
            estado_auto = "VACÍO" if self.autos_en_taller[i] is None else self.autos_en_taller[i]
            ctk.CTkLabel(slot_frame, text=estado_auto, pady=50).pack()
            
            ctk.CTkButton(slot_frame, text="Gestionar", state="disabled" if not self.autos_en_taller[i] else "normal").pack(pady=10)

        # 3. BARRA INFERIOR (Acciones)
        footer = ctk.CTkFrame(self.ventana_actual, height=100)
        footer.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(footer, text="🛒 BUSCAR AUTOS USADOS", width=250, height=50).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(footer, text="🛠️ VER TRABAJOS CLIENTES", width=250, height=50, fg_color="#3498db").pack(side="right", padx=20, pady=10)

        self.ventana_actual.mainloop()

if __name__ == "__main__":
    JuegoTaller()