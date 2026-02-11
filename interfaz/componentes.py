import customtkinter as ctk

class SlotTaller(ctk.CTkFrame):
    def __init__(self, master, titulo, color, juego=None, **kwargs):
        super().__init__(master, fg_color=color, border_width=2, **kwargs)
        self.juego = juego
        self.titulo = titulo
        # Label del Título (ELEVADOR / PARKING)
        ctk.CTkLabel(self, text=self.titulo, font=("Arial", 14, "bold")).pack(pady=10)
        
        # Label del Estado del Auto
        self.label_auto = ctk.CTkLabel(self, text="VACÍO", font=("Arial", 12))
        self.label_auto.pack(pady=40)
        
        # Botón de acción
        self.btn_gestionar = ctk.CTkButton(self, text="Gestionar", state="disabled", width=140)
        self.btn_gestionar.pack(pady=10, padx=10)

    def actualizar(self, auto):
        self.auto_actual = auto # Guardamos la referencia del auto
        if auto:
            self.label_auto.configure(text=f"{auto.marca}\n{auto.modelo}\nMotor: {auto.partes['Motor']}%", text_color="white")
            self.btn_gestionar.configure(state="normal", command=self.abrir_inspeccion) # Agregamos el comando
        else:
            self.label_auto.configure(text="VACÍO", text_color="gray")
            self.btn_gestionar.configure(state="disabled")

    def abrir_inspeccion(self):
        # Ventana unificada de detalles del auto
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Diagnóstico: {self.auto_actual.marca} {self.auto_actual.modelo}")
        ventana.geometry("400x600")
        ventana.after(10, ventana.lift)

        ctk.CTkLabel(ventana, text="ESTADO DE COMPONENTES", font=("Arial", 18, "bold")).pack(pady=20)

        for parte, estado in self.auto_actual.partes.items():
            f = ctk.CTkFrame(ventana, fg_color="transparent")
            f.pack(fill="x", padx=30, pady=5)
            
            ctk.CTkLabel(f, text=f"{parte}:").pack(side="left")
            
            bar = ctk.CTkProgressBar(f, width=150)
            bar.set(estado / 100)
            bar.pack(side="right")
            
            # Colores dinámicos según el desgaste
            if estado < 30:
                bar.configure(progress_color="#e74c3c") # Rojo
            elif estado < 70:
                bar.configure(progress_color="#f1c40f") # Amarillo
            else:
                bar.configure(progress_color="#2ecc71") # Verde

        ctk.CTkButton(ventana, text="CERRAR", command=ventana.destroy).pack(pady=20)