import customtkinter as ctk
import random
from modelos.auto import Auto
from tkinter import messagebox

class VentanaMercado(ctk.CTkToplevel):
    def __init__(self, master, motor, callback_actualizar):
        super().__init__(master)
        self.motor = motor
        self.callback_actualizar = callback_actualizar # Para refrescar el taller al comprar
        
        self.title("Mercado de Autos Usados")
        self.geometry("600x400")
        self.after(10, self.lift) # Truco para que la ventana aparezca al frente en Linux

        ctk.CTkLabel(self, text="OFERTAS DEL DÍA", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.contenedor_autos = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_autos.pack(expand=True, fill="both", padx=20)
        
        self.generar_ofertas()

    def generar_ofertas(self):
        pool_modelos = Auto.cargar_modelos_desde_csv()
        
        # Elegimos 3 al azar de la lista del CSV
        ofertas_elegidas = random.sample(pool_modelos, k=min(3, len(pool_modelos)))

        for marca, modelo, precio_base in ofertas_elegidas:
            auto_oferta = Auto(marca, modelo, precio_base)
            
            frame_oferta = ctk.CTkFrame(self.contenedor_autos)
            frame_oferta.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            
            ctk.CTkLabel(frame_oferta, text=f"{marca}\n{modelo}", font=("Arial", 14, "bold")).pack(pady=10)
            ctk.CTkLabel(frame_oferta, text=f"Precio: ${precio_base}", text_color="#2ecc71").pack()
            ctk.CTkLabel(frame_oferta, text=f"Motor: {auto_oferta.partes['Motor']}%").pack()

            btn = ctk.CTkButton(frame_oferta, text="Comprar", 
                                command=lambda a=auto_oferta: self.intentar_compra(a))
            btn.pack(pady=15, padx=10)

    def intentar_compra(self, auto):
        exito, mensaje = self.motor.comprar_auto(auto)
        if exito:
            messagebox.showinfo("Compra exitosa", mensaje, parent=self)
            self.callback_actualizar()
            self.destroy()
        else:
            messagebox.showerror("Compra fallida", mensaje, parent=self)