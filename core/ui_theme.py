import customtkinter as ctk

# Estilo base para toda la UI
COLORS = {
    "bg": "#0f1115",
    "panel": "#151a21",
    "panel_alt": "#1b2330",
    "card": "#1c2430",
    "accent": "#3b82f6",
    "accent_2": "#22c55e",
    "danger": "#ef4444",
    "text": "#e5e7eb",
    "muted": "#9ca3af",
}

FONTS = {
    "title": ("Arial", 26, "bold"),
    "subtitle": ("Arial", 16, "bold"),
    "body": ("Arial", 12),
    "small": ("Arial", 11),
}


def apply_theme(root=None):
    ctk.set_appearance_mode("Dark")
    # Si se necesita root para ajustes extra, se puede usar acá
    return True
