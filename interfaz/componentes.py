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
        self.auto_actual = auto # Guardamos la referencia del auto
        if auto:
            self.label_auto.configure(text=f"{auto.marca}\n{auto.modelo}\nMotor: {auto.partes['Motor']}%", text_color="white")
            self.btn_gestionar.configure(state="normal", command=self.abrir_inspeccion) # Agregamos el comando
        else:
            self.label_auto.configure(text="VACÍO", text_color="gray")
            self.btn_gestionar.configure(state="disabled")

    def abrir_inspeccion(self):
        # Esta es la ventana de detalles que mencionamos antes
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Diagnóstico: {self.auto_actual.marca}")
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
            if estado < 30: bar.configure(progress_color="#e74c3c") # Rojo
            elif estado < 70: bar.configure(progress_color="#f1c40f") # Amarillo
            else: bar.configure(progress_color="#2ecc71") # Verde
            
    def mostrar_detalles_auto(self, auto):
        ventana_info = ctk.CTkToplevel(self)
        ventana_info.title(f"Inspeccionando: {auto.marca} {auto.modelo}")
        ventana_info.geometry("400x550")
        ventana_info.after(10, ventana_info.lift)

        ctk.CTkLabel(ventana_info, text="INFORME DE ESTADO", font=("Arial", 20, "bold")).pack(pady=20)

        # Creamos una barrita de progreso por cada pieza
        for parte, estado in auto.partes.items():
            frame_parte = ctk.CTkFrame(ventana_info, fg_color="transparent")
            frame_parte.pack(fill="x", padx=30, pady=5)
            
            ctk.CTkLabel(frame_parte, text=f"{parte}: {estado}%").pack(side="left")
            
            # Barra de progreso (0.0 a 1.0)
            progreso = ctk.CTkProgressBar(frame_parte, width=150)
            progreso.set(estado / 100)
            progreso.pack(side="right")
            
            # Color según estado
            if estado < 40: progreso.configure(progress_color="red")
            elif estado < 75: progreso.configure(progress_color="yellow")
            else: progreso.configure(progress_color="green")

        ctk.CTkButton(ventana_info, text="CERRAR", command=ventana_info.destroy).pack(pady=20)