import customtkinter as ctk

class SlotTaller(ctk.CTkFrame):
    def __init__(self, master, titulo, color, **kwargs):
        super().__init__(master, fg_color=color, border_width=2, **kwargs)
        
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
        if auto:
            self.label_auto.configure(text=f"{auto.marca}\n{auto.modelo}\nMotor: {auto.motor}%", text_color="white")
            self.btn_gestionar.configure(state="normal")
        else:
            self.label_auto.configure(text="VACÍO", text_color="gray")
            self.btn_gestionar.configure(state="disabled")