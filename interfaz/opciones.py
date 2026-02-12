import customtkinter as ctk
from core.ui_theme import COLORS, FONTS
import core.config as cfg

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver, db=None):
        super().__init__(master)
        self.al_volver = al_volver
        self.db = db
        self.configure(fg_color=COLORS["bg"])
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="CONFIGURACIÓN", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=20)

        # MODO OSCURO/CLARO
        ctk.CTkLabel(self, text="Tema:", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=5)
        self.tema = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                           command=self.cambiar_tema)
        self.tema.pack(pady=10)
        if self.db:
            self.tema.set(self.db.get_config("tema", ctk.get_appearance_mode()))
        else:
            self.tema.set(ctk.get_appearance_mode())

        # PANTALLA COMPLETA
        full_default = False
        if self.db:
            full_default = str(self.db.get_config("fullscreen", "false")).lower() == "true"
        self.full_var = ctk.BooleanVar(value=full_default)
        ctk.CTkCheckBox(self, text="Pantalla Completa", variable=self.full_var,
                        command=self.toggle_full).pack(pady=14)

        # VOLUMEN / MUTE
        ctk.CTkLabel(self, text="Sonido:", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(6, 2))
        vol_default = 1.0
        if self.db:
            try:
                vol_default = float(self.db.get_config("volume", "1.0"))
            except Exception:
                vol_default = 1.0
        self.vol_var = ctk.DoubleVar(value=vol_default)
        self.scroll_vol = ctk.CTkSlider(self, from_=0.0, to=1.0, number_of_steps=20, variable=self.vol_var,
                                        command=self._on_volume_change)
        self.scroll_vol.pack(pady=6)

        self.mute_var = ctk.BooleanVar(value=(str(self.db.get_config("mute", "false")).lower() == "true") if self.db else False)
        ctk.CTkCheckBox(self, text="Silenciar", variable=self.mute_var, command=self._on_mute_toggle).pack(pady=6)

        # BALANCE DEL JUEGO (avanzado)
        ctk.CTkLabel(self, text="Balance (avanzado):", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(10, 4))

        # EXP_PER_POINT_DIVISOR (int)
        exp_default = cfg.EXP_PER_POINT_DIVISOR
        if self.db:
            try:
                exp_default = int(self.db.get_config("EXP_PER_POINT_DIVISOR", exp_default))
            except Exception:
                exp_default = cfg.EXP_PER_POINT_DIVISOR
        ctk.CTkLabel(self, text="EXP por puntos reparados:", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(6, 2))
        self.exp_var = ctk.IntVar(value=exp_default)
        self.exp_spin = ctk.CTkEntry(self, width=80, textvariable=self.exp_var)
        self.exp_spin.pack(pady=(0, 6))

        # LEVEL_SELL_MULTIPLIER (float)
        lvl_default = cfg.LEVEL_SELL_MULTIPLIER
        if self.db:
            try:
                lvl_default = float(self.db.get_config("LEVEL_SELL_MULTIPLIER", lvl_default))
            except Exception:
                lvl_default = cfg.LEVEL_SELL_MULTIPLIER
        ctk.CTkLabel(self, text="Multiplicador por nivel (venta):", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(6, 2))
        self.lvl_var = ctk.DoubleVar(value=lvl_default)
        self.lvl_slider = ctk.CTkSlider(self, from_=0.0, to=1.0, number_of_steps=100, variable=self.lvl_var,
                                        command=lambda v: None)
        self.lvl_slider.set(lvl_default)
        self.lvl_slider.pack(pady=6)

        # REPAIR_COST_PER_POINT and REPAIR_COST_CAP_MULTIPLIER
        rcp_default = cfg.REPAIR_COST_PER_POINT
        rcap_default = cfg.REPAIR_COST_CAP_MULTIPLIER
        if self.db:
            try:
                rcp_default = float(self.db.get_config("REPAIR_COST_PER_POINT", rcp_default))
            except Exception:
                rcp_default = cfg.REPAIR_COST_PER_POINT
            try:
                rcap_default = float(self.db.get_config("REPAIR_COST_CAP_MULTIPLIER", rcap_default))
            except Exception:
                rcap_default = cfg.REPAIR_COST_CAP_MULTIPLIER

        ctk.CTkLabel(self, text="Costo por punto (reparación):", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(6, 2))
        self.rcp_var = ctk.DoubleVar(value=rcp_default)
        self.rcp_entry = ctk.CTkEntry(self, width=120, textvariable=self.rcp_var)
        self.rcp_entry.pack(pady=4)

        ctk.CTkLabel(self, text="Tope de reparación (multiplicador):", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=(6, 2))
        self.rcap_var = ctk.DoubleVar(value=rcap_default)
        self.rcap_entry = ctk.CTkEntry(self, width=120, textvariable=self.rcap_var)
        self.rcap_entry.pack(pady=(0, 6))

        ctk.CTkButton(self, text="Aplicar balance", fg_color=COLORS["accent_2"], command=self._apply_balance_changes).pack(pady=(4,8))

        ctk.CTkButton(self, text="⬅️ VOLVER", fg_color=COLORS["panel_alt"], hover_color="#253041",
                  command=self.al_volver).pack(pady=20)

    def toggle_full(self):
        ventana = self.winfo_toplevel()
        ventana.attributes("-fullscreen", self.full_var.get())
        if self.db:
            self.db.set_config("fullscreen", "true" if self.full_var.get() else "false")

    def _apply_balance_changes(self):
        # read and save to DB and apply to runtime config
        try:
            exp_v = int(self.exp_var.get())
            lvl_v = float(self.lvl_var.get())
            rcp_v = float(self.rcp_var.get())
            rcap_v = float(self.rcap_var.get())
        except Exception:
            return

        # persist
        if self.db:
            self.db.set_config("EXP_PER_POINT_DIVISOR", str(exp_v))
            self.db.set_config("LEVEL_SELL_MULTIPLIER", str(lvl_v))
            self.db.set_config("REPAIR_COST_PER_POINT", str(rcp_v))
            self.db.set_config("REPAIR_COST_CAP_MULTIPLIER", str(rcap_v))

        # apply at runtime
        try:
            cfg.apply_runtime_override("EXP_PER_POINT_DIVISOR", exp_v)
            cfg.apply_runtime_override("LEVEL_SELL_MULTIPLIER", lvl_v)
            cfg.apply_runtime_override("REPAIR_COST_PER_POINT", rcp_v)
            cfg.apply_runtime_override("REPAIR_COST_CAP_MULTIPLIER", rcap_v)
        except Exception:
            pass

        # feedback
        try:
            from tkinter import messagebox
            messagebox.showinfo("Opciones", "Balance actualizado.")
        except Exception:
            pass

    def _on_volume_change(self, v):
        if self.db:
            self.db.set_config("volume", str(float(v)))
        try:
            from core.sound_manager import get_sound_manager
            sm = get_sound_manager()
            sm.set_volume(float(v))
        except Exception:
            pass

    def _on_mute_toggle(self):
        if self.db:
            self.db.set_config("mute", "true" if self.mute_var.get() else "false")
        try:
            from core.sound_manager import get_sound_manager
            sm = get_sound_manager()
            sm.set_muted(self.mute_var.get())
        except Exception:
            pass

    def cambiar_tema(self, valor):
        ctk.set_appearance_mode(valor)
        if self.db:
            self.db.set_config("tema", valor)