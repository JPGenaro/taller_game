import customtkinter as ctk
from core.database import Database
from core.motor import Motor
from modelos.auto import Auto
from interfaz.mercado import VentanaMercado
from interfaz.componentes import SlotTaller
from interfaz.opciones import VentanaOpciones
from interfaz.pausa import MenuPausa  # Asegúrate de tener este archivo creado
from tkinter import messagebox, simpledialog
from core.ui_theme import COLORS, FONTS, apply_theme

class Aplicacion:
    def __init__(self):
        # 1. Configuración de Ventana
        self.root = ctk.CTk()
        self.root.title("Garage Tycoon v0.3")
        self.root.geometry("1000x700")
        self.root.configure(fg_color=COLORS["bg"])
        
        # 2. Inicialización de Núcleo (Core)
        self.db = Database()
        self.motor = Motor()

        # Aplicar configuración persistida (tema, fullscreen)
        apply_theme(self.root)
        self.aplicar_configuracion()
        
        # 3. Estado de la sesión actual
        self.slot_actual = None
        
        # Iniciar juego
        self.mostrar_menu_inicio()
        self.root.mainloop()

    # --- UTILIDADES ---
    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- FLUJO DE NAVEGACIÓN (Pantallas Principales) ---

    def mostrar_menu_inicio(self):
        """Pantalla de título y menú principal."""
        self.limpiar_pantalla()
        
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(pady=30)
        ctk.CTkLabel(header, text="GARAGE TYCOON", font=("Arial Bold", 50), text_color=COLORS["text"]).pack()
        ctk.CTkLabel(header, text="Compra, repara y vende autos", font=FONTS["body"], text_color=COLORS["muted"]).pack(pady=6)
        
        btn_container = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_container.pack(expand=True)

        # Botones Principales
        ctk.CTkButton(btn_container, text="NUEVA PARTIDA", width=260, height=46,
                  fg_color=COLORS["accent"], hover_color="#2563eb",
                      command=lambda: self.mostrar_seleccion_slot("nueva")).pack(pady=10)
        
        # Cargar partida (solo si hay datos)
        estado_cargar = "normal" if self.db.hay_partidas_guardadas() else "disabled"
        ctk.CTkButton(btn_container, text="CARGAR PARTIDA", width=260, height=46, state=estado_cargar,
                  fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=lambda: self.mostrar_seleccion_slot("cargar")).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="OPCIONES", width=260, height=46,
                  fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.mostrar_opciones).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="CRÉDITOS", width=260, height=46,
                  fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.mostrar_creditos).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="SALIR", width=260, height=46, fg_color=COLORS["danger"],
                  hover_color="#dc2626",
                      command=self.root.quit).pack(pady=10)

    def mostrar_seleccion_slot(self, modo: str):
        """Pantalla de selección entre los 3 slots de guardado."""
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text=f"SELECCIONAR SLOT ({modo.upper()})", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=30)

        for i in range(1, 4):
            datos = self.db.obtener_resumen_partida(i)
            frame = ctk.CTkFrame(self.root, fg_color=COLORS["panel"], corner_radius=12)
            frame.pack(fill="x", padx=50, pady=10)

            info = f"Slot {i}: {datos['personaje']} (Nivel {datos['nivel']})" if datos else f"Slot {i}: VACÍO"
            ctk.CTkLabel(frame, text=info, font=FONTS["body"], text_color=COLORS["text"]).pack(side="left", padx=20, pady=15)

            # Lógica de botón según modo
            btn_text = "ELEGIR" if modo == "nueva" else "CARGAR"
            btn_state = "normal" if (modo == "nueva" or datos) else "disabled"
            
            ctk.CTkButton(frame, text=btn_text, state=btn_state,
                          fg_color=COLORS["accent"], hover_color="#2563eb",
                          command=lambda s=i: self.inicializar_partida(s, modo)).pack(side="right", padx=20)

        ctk.CTkButton(self.root, text="VOLVER", fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.mostrar_menu_inicio).pack(pady=20)

    def mostrar_creditos(self):
        """Pantalla de agradecimientos y autoría."""
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self.root, text="CRÉDITOS", font=("Arial Bold", 40), text_color=COLORS["text"]).pack(pady=40)
        
        info_frame = ctk.CTkFrame(self.root, fg_color=COLORS["panel"], corner_radius=12)
        info_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        texto_creditos = (
            "DESARROLLADO POR:\nJP Genaro\n\n"
            "TECNOLOGÍAS:\nPython 3.12 & CustomTkinter\n\n"
            "AGRADECIMIENTOS:\nA la comunidad de dev de Pop!_OS\ny a vos por jugar."
        )
        
        ctk.CTkLabel(info_frame, text=texto_creditos, font=("Arial", 18), text_color=COLORS["text"]).pack(expand=True)
        
        ctk.CTkButton(self.root, text="VOLVER AL MENÚ", width=200, fg_color=COLORS["panel_alt"], hover_color="#253041",
                      command=self.mostrar_menu_inicio).pack(pady=30)
        
    # --- LÓGICA DE PARTIDA ---

    def inicializar_partida(self, slot_id, modo):
        """Configura el motor y la base de datos para la sesión."""
        self.slot_actual = slot_id
        if modo == "nueva":
            self.mostrar_registro()
        else:
            datos = self.db.cargar_partida(slot_id)
            self.motor.cargar_datos(datos)
            self.mostrar_taller()

    def mostrar_registro(self):
        """Pantalla para nombrar personaje y taller al crear partida nueva."""
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text="DATOS DEL PROPIETARIO", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=30)
        
        ent_nombre = ctk.CTkEntry(self.root, placeholder_text="Tu Nombre", width=320)
        ent_nombre.pack(pady=10)
        ent_taller = ctk.CTkEntry(self.root, placeholder_text="Nombre del Taller", width=320)
        ent_taller.pack(pady=10)

        def confirmar():
            if ent_nombre.get() and ent_taller.get():
                self.motor.personaje = ent_nombre.get()
                self.motor.taller = ent_taller.get()
                # Guardar y solo pasar a taller si se guardó con éxito
                guardado = self.guardar_partida(self.slot_actual)  # no pasar ventana inexistente
                if guardado:
                    self.mostrar_taller()

        ctk.CTkButton(self.root, text="COMENZAR AVENTURA", fg_color=COLORS["accent"], hover_color="#2563eb",
                  command=confirmar).pack(pady=30)

    def mostrar_taller(self):
        """Interfaz principal del taller de reparaciones (Elevadores y Parking)."""
        self.limpiar_pantalla()
        
        # --- HEADER (Info del Jugador) ---
        header = ctk.CTkFrame(self.root, height=60, fg_color=COLORS["panel"], corner_radius=12)
        header.pack(fill="x", side="top", padx=10, pady=5)
        
        # Mostrar nombre de personaje y nombre del taller juntos a la izquierda
        nombre_personaje = getattr(self.motor, "personaje", "Jugador")
        nombre_taller = getattr(self.motor, "taller", "Mi Taller")
        ctk.CTkLabel(header, text=f"👤 {nombre_personaje}   |   🏠 {nombre_taller}", font=("Arial", 16, "bold"), text_color=COLORS["text"]).pack(side="left", padx=20)
        
        ctk.CTkLabel(header, text=f"💰 ${self.motor.dinero}", text_color=COLORS["accent_2"], font=("Arial", 16, "bold")).pack(side="right", padx=20)
        
        # Botón de Pausa (engranaje)
        ctk.CTkButton(header, text="⚙️", width=40, fg_color=COLORS["panel_alt"], hover_color="#253041",
                  command=self.abrir_pausa).pack(side="right", padx=10)

        # --- INFO DE NIVEL / XP (mantener el resto igual; agregado aquí) ---
        try:
            xp_actual, xp_req, xp_faltante, porcentaje = self.motor.progreso_nivel()
        except Exception:
            xp_actual, xp_req, xp_faltante, porcentaje = 0, 100, 100, 0.0

        info_nivel = ctk.CTkFrame(self.root, height=40, fg_color=COLORS["panel"], corner_radius=10)
        info_nivel.pack(fill="x", padx=12, pady=(4,10))
        ctk.CTkLabel(info_nivel, text=f"Nivel: {getattr(self.motor, 'nivel', 1)}", font=("Arial", 12, "bold"), text_color=COLORS["text"]).pack(side="left", padx=8)
        ctk.CTkLabel(info_nivel, text=f"XP: {xp_actual} / {xp_req}  (faltan {xp_faltante})", font=("Arial", 11), text_color=COLORS["muted"]).pack(side="left", padx=8)
        barra_xp = ctk.CTkProgressBar(info_nivel, width=300)
        barra_xp.set(porcentaje)
        barra_xp.pack(side="right", padx=12)

        # --- ZONA DE TRABAJO (Elevadores) ---
        zona_elevadores = ctk.CTkFrame(self.root, fg_color="transparent")
        zona_elevadores.pack(expand=True, fill="both", padx=20, pady=10)

        # Pasamos: master, titulo y color (como pide tu interfaz/componentes.py)
        for i in range(2): 
            slot_ui = SlotTaller(zona_elevadores, titulo=f"ELEVADOR {i+1}", color=COLORS["card"], juego=self, slot_index=i) 
            slot_ui.actualizar(self.motor.slots[i])
            slot_ui.pack(side="left", expand=True, fill="both", padx=10)

        # --- ZONA DE PARKING ---
        zona_parking = ctk.CTkFrame(self.root, height=150, fg_color="transparent")
        zona_parking.pack(fill="x", padx=20, pady=10)

        # Pasamos: master, titulo y color
        slot_parking = SlotTaller(zona_parking, titulo="ESTACIONAMIENTO", color=COLORS["panel_alt"], juego=self, slot_index=2)
        slot_parking.actualizar(self.motor.slots[2])
        slot_parking.pack(side="left", expand=True, fill="both", padx=10)
        
        # --- FOOTER (Navegación) ---
        footer = ctk.CTkFrame(self.root, height=70, fg_color=COLORS["panel"], corner_radius=12)
        footer.pack(fill="x", side="bottom", pady=10)
        
        ctk.CTkButton(footer, text="🛒 IR AL MERCADO", height=45, width=200,
                  fg_color=COLORS["accent"], hover_color="#2563eb",
                      command=self.abrir_mercado).pack(expand=True)
        
    # --- MODALES Y VENTANAS SECUNDARIAS ---

    def abrir_pausa(self):
        """Muestra el menú de pausa (flotante)."""
        MenuPausa(self.root, self)

    def mostrar_opciones(self):
        """Pantalla de ajustes técnicos."""
        self.limpiar_pantalla()
        VentanaOpciones(self.root, al_volver=self.mostrar_menu_inicio, db=self.db)

    def abrir_mercado(self):
        """Abre la ventana de compra de autos."""
        VentanaMercado(self.root, self.motor, self.mostrar_taller)

    def aplicar_configuracion(self):
        tema = self.db.get_config("tema", "Dark")
        try:
            ctk.set_appearance_mode(tema)
        except Exception:
            ctk.set_appearance_mode("Dark")

        fullscreen = self.db.get_config("fullscreen", "false")
        modo_full = str(fullscreen).lower() == "true"
        try:
            self.root.attributes("-fullscreen", modo_full)
        except Exception:
            pass

    def guardar_partida(self, slot: int | None = None, parent_window=None):
        """
        Guarda la partida en DB y muestra un mensaje informando el resultado.
        Si no se pasa slot pide al usuario que seleccione un slot.
        parent_window: si se pasa, se destruirá antes de mostrar el mensaje.
        """
        # Forzar foco para evitar que el messagebox quede detrás
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.root.update()
        except Exception:
            pass

        slot_to_use = slot if slot is not None else self.slot_actual
        if slot_to_use is None:
            slot_chosen = simpledialog.askinteger(
                "Elegir slot",
                "Elegí un slot para guardar (1-3):",
                parent=self.root,
                minvalue=1,
                maxvalue=3
            )
            if slot_chosen is None:
                return False
            slot_to_use = slot_chosen

        try:
            self.db.guardar_partida(slot_to_use, self.motor)
            self.slot_actual = slot_to_use

            # Si nos pasan una ventana modal, cerrarla primero para que el dialogo sea visible
            try:
                if parent_window is not None:
                    parent_window.destroy()
            except Exception:
                pass

            # Mostrar el messagebox con un small delay para asegurar el foco y orden de ventanas
            def _show_ok():
                try:
                    messagebox.showinfo("Guardar partida", f"Partida guardada en el slot {slot_to_use}.", parent=self.root)
                except Exception:
                    # fallback sin parent
                    messagebox.showinfo("Guardar partida", f"Partida guardada en el slot {slot_to_use}.")

            self.root.after(120, _show_ok)
            return True
        except Exception as e:
            # Cerrar modal si existe antes de error
            try:
                if parent_window is not None:
                    parent_window.destroy()
            except Exception:
                pass

            def _show_err():
                try:
                    messagebox.showerror("Error al guardar", f"No se pudo guardar la partida:\n{e}", parent=self.root)
                except Exception:
                    messagebox.showerror("Error al guardar", f"No se pudo guardar la partida:\n{e}")
            self.root.after(120, _show_err)
            return False

if __name__ == "__main__":
    Aplicacion()