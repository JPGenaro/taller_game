import customtkinter as ctk
import random
from modelos.auto import Auto
from tkinter import messagebox
from core.ui_theme import COLORS, FONTS
from core.config import ConfigManager
from PIL import Image
from core.sound_manager import get_sound_manager

class VentanaMercado(ctk.CTkToplevel):
    def __init__(self, master, motor, callback_actualizar):
        super().__init__(master)
        self.motor = motor
        self.callback_actualizar = callback_actualizar # Para refrescar el taller al comprar
        # cargar icono de compra (opcional)
        self._icon_small = None
        try:
            ruta_icon = ConfigManager.data_path("icon_buy.png")
            if ruta_icon and os.path.exists(ruta_icon):
                img_icon = Image.open(ruta_icon).convert("RGBA")
                self._icon_small = ctk.CTkImage(light_image=img_icon, dark_image=img_icon, size=(20, 20))
        except Exception:
            self._icon_small = None

        self.title("Mercado de Autos Usados")
        self.geometry("760x460")
        self.configure(fg_color=COLORS["bg"])
        self.after(10, self.lift) # Truco para que la ventana aparezca al frente en Linux

        ctk.CTkLabel(self, text="OFERTAS DEL DÍA", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=18)
        
        self.contenedor_autos = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_autos.pack(expand=True, fill="both", padx=20)
        
        self.sound = get_sound_manager()
        self.generar_ofertas()

    def generar_ofertas(self):
        pool_modelos = Auto.cargar_modelos_desde_csv()
        
        # Elegimos 3 al azar de la lista del CSV
        ofertas_elegidas = random.sample(pool_modelos, k=min(3, len(pool_modelos)))

        for marca, modelo, precio_base in ofertas_elegidas:
            auto_oferta = Auto(marca, modelo, precio_base)
            
            frame_oferta = ctk.CTkFrame(self.contenedor_autos, fg_color=COLORS["card"], corner_radius=12)
            frame_oferta.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            
            ctk.CTkLabel(frame_oferta, text=f"{marca}\n{modelo}", font=FONTS["subtitle"], text_color=COLORS["text"]).pack(pady=(14, 8))
            ctk.CTkLabel(frame_oferta, text=f"Precio: ${precio_base}", text_color=COLORS["accent_2"], font=FONTS["body"]).pack()
            ctk.CTkLabel(frame_oferta, text=f"KM: {auto_oferta.km}", text_color=COLORS["muted"], font=FONTS["small"]).pack()
            ctk.CTkLabel(frame_oferta, text=f"Motor: {auto_oferta.partes['Motor']}%", text_color=COLORS["muted"], font=FONTS["small"]).pack()
            ctk.CTkLabel(frame_oferta, text=f"Valor venta: ${auto_oferta.valor_venta()}", text_color=COLORS["text"], font=FONTS["small"]).pack(pady=(0, 6))

            # usar icono si está disponible
            btn_kwargs = {"fg_color": COLORS["accent"], "hover_color": "#2563eb", "command": lambda a=auto_oferta: self._comprar_con_efecto(a)}
            if self._icon_small is not None:
                btn_kwargs["image"] = self._icon_small
            btn = ctk.CTkButton(frame_oferta, text="Comprar", **btn_kwargs)
            btn.pack(pady=15, padx=10)
            # animación pulse simple
            self._pulse_button(btn)

    def intentar_compra(self, auto):
        exito, mensaje = self.motor.comprar_auto(auto)
        if exito:
            # sonido opcional
            try:
                self.sound.play("sound_buy.wav")
            except Exception:
                pass
            messagebox.showinfo("Compra exitosa", mensaje, parent=self)
            self.callback_actualizar()
            self.destroy()
        else:
            messagebox.showerror("Compra fallida", mensaje, parent=self)

    def _comprar_con_efecto(self, auto):
        # pequeña envoltura para intentar reproducir sonido antes/after
        try:
            self.sound.play("sound_buy.wav")
        except Exception:
            pass
        self.intentar_compra(auto)

    def _pulse_button(self, btn, step=0):
        # alterna levemente la opacidad simulada por cambiar color entre 2 tonos
        try:
            if step % 2 == 0:
                btn.configure(fg_color="#2b6ef6")
            else:
                btn.configure(fg_color=COLORS["accent"])
            btn.after(700, lambda: self._pulse_button(btn, step+1))
        except Exception:
            pass