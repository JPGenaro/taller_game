import customtkinter as ctk
from tkinter import messagebox
from core.ui_theme import COLORS, FONTS

class SlotTaller(ctk.CTkFrame):
    def __init__(self, master, titulo, color, juego=None, slot_index=None, **kwargs):
        super().__init__(master, fg_color=color, border_width=2, border_color="#263141", corner_radius=12, **kwargs)
        self.juego = juego
        self.titulo = titulo
        self.slot_index = slot_index
        # Label del Título (ELEVADOR / PARKING)
        ctk.CTkLabel(self, text=self.titulo, font=FONTS["subtitle"], text_color=COLORS["text"]).pack(pady=10)
        
        # Label del Estado del Auto
        self.label_auto = ctk.CTkLabel(self, text="VACÍO", font=FONTS["body"], text_color=COLORS["muted"])
        self.label_auto.pack(pady=40)
        
        # Botón de acción
        self.btn_gestionar = ctk.CTkButton(self, text="Gestionar", state="disabled", width=140,
                           fg_color=COLORS["accent"], hover_color="#2563eb")
        self.btn_gestionar.pack(pady=10, padx=10)

    def actualizar(self, auto):
        self.auto_actual = auto # Guardamos la referencia del auto
        if auto:
            self.label_auto.configure(text=f"{auto.marca}\n{auto.modelo}\nKM: {auto.km}\nMotor: {auto.partes['Motor']}%", text_color=COLORS["text"])
            self.btn_gestionar.configure(state="normal", command=self.abrir_inspeccion) # Agregamos el comando
        else:
            self.label_auto.configure(text="VACÍO", text_color="gray")
            self.btn_gestionar.configure(state="disabled")

    def abrir_inspeccion(self):
        # Ventana unificada de detalles del auto
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Diagnóstico: {self.auto_actual.marca} {self.auto_actual.modelo}")
        # Abrir en fullscreen para mantener consistencia
        try:
            ventana.attributes("-fullscreen", True)
        except Exception:
            ventana.geometry("460x620")
        ventana.configure(fg_color=COLORS["bg"])
        ventana.after(10, ventana.lift)

        ctk.CTkLabel(ventana, text="ESTADO DE COMPONENTES", font=FONTS["subtitle"], text_color=COLORS["text"]).pack(pady=(16, 6))

        info = ctk.CTkLabel(ventana, text=f"KM: {self.auto_actual.km}  |  Año: {getattr(self.auto_actual, 'anio', 'N/A')}  |  Valor venta: ${self.auto_actual.valor_venta()}", font=FONTS["small"], text_color=COLORS["muted"])
        info.pack(pady=(0, 6))

        scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLORS["panel"], height=380)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        for parte, estado in self.auto_actual.partes.items():
            f = ctk.CTkFrame(scroll, fg_color=COLORS["panel_alt"], corner_radius=10)
            f.pack(fill="x", padx=8, pady=5)
            
            ctk.CTkLabel(f, text=f"{parte}:", text_color=COLORS["text"], font=FONTS["small"]).pack(side="left", padx=8)
            
            bar = ctk.CTkProgressBar(f, width=170)
            bar.set(estado / 100)
            bar.pack(side="right", padx=8, pady=6)
            
            # Colores dinámicos según el desgaste
            if estado < 30:
                bar.configure(progress_color="#e74c3c") # Rojo
            elif estado < 70:
                bar.configure(progress_color="#f1c40f") # Amarillo
            else:
                bar.configure(progress_color="#2ecc71") # Verde

        # Acciones siempre visibles
        acciones = ctk.CTkFrame(ventana, fg_color="transparent")
        acciones.pack(pady=(0, 10))

        ctk.CTkButton(acciones, text="Reparar todo", fg_color=COLORS["accent_2"],
                      command=lambda: self._reparar_total(ventana)).pack(side="left", padx=8)
        ctk.CTkButton(acciones, text="Vender auto", fg_color=COLORS["danger"],
                      command=lambda: self._vender_auto(ventana)).pack(side="left", padx=8)

        ctk.CTkButton(ventana, text="CERRAR", fg_color=COLORS["panel_alt"], hover_color="#253041",
                  command=ventana.destroy).pack(pady=(0, 12))

    def _reparar_total(self, ventana):
        if self.juego is None or self.slot_index is None:
            return
        ok, msg = self.juego.motor.reparar_auto_total(self.slot_index)
        if ok:
            messagebox.showinfo("Reparación", msg, parent=ventana)
            self.juego.mostrar_taller()
            ventana.destroy()
        else:
            messagebox.showerror("Reparación", msg, parent=ventana)

    def _vender_auto(self, ventana):
        if self.juego is None or self.slot_index is None:
            return
        ok, msg = self.juego.motor.vender_auto(self.slot_index)
        if ok:
            messagebox.showinfo("Venta", msg, parent=ventana)
            self.juego.mostrar_taller()
            ventana.destroy()
        else:
            messagebox.showerror("Venta", msg, parent=ventana)