import customtkinter as ctk
import threading

from core.ui_theme import COLORS, FONTS


def show_message(parent, title: str, message: str, kind: str = "info", duration: float | None = None):
    """Show a centered, styled message near the top of the app.

    - kind: 'info' | 'success' | 'error'
    - duration: seconds to auto-dismiss (None => require OK for errors, default 2.5s for info)
    """
    try:
        top = ctk.CTkToplevel(parent)
    except Exception:
        # fallback: try parent.winfo_toplevel()
        try:
            top = ctk.CTkToplevel(parent.winfo_toplevel())
        except Exception:
            return

    try:
        top.overrideredirect(True)
    except Exception:
        pass
    top.attributes("-topmost", True)
    top.configure(fg_color="transparent")

    frame = ctk.CTkFrame(top, fg_color=COLORS.get("panel" , "#222222"), corner_radius=12)
    frame.pack(padx=8, pady=8)

    # color by kind
    if kind == "error":
        color = COLORS.get("danger", "#c0392b")
    elif kind == "success":
        color = COLORS.get("accent_2", "#16a34a")
    else:
        color = COLORS.get("accent", "#3b82f6")

    ctk.CTkLabel(frame, text=title, font=(FONTS.get("title", ("Arial", 16))), text_color=color).pack(padx=12, pady=(8, 2))
    ctk.CTkLabel(frame, text=message, font=FONTS.get("body", ("Arial", 12)), text_color=COLORS.get("text")).pack(padx=12, pady=(0, 8))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(0,8))

    dismissed = threading.Event()

    def _close():
        try:
            top.destroy()
        except Exception:
            pass
        dismissed.set()

    if kind == "error" or duration is None:
        # require OK
        ctk.CTkButton(btn_frame, text="OK", fg_color=COLORS.get("panel_alt"), command=_close).pack()
    else:
        # show a subtle close button but auto-dismiss
        ctk.CTkButton(btn_frame, text="Cerrar", fg_color=COLORS.get("panel_alt"), command=_close).pack()
        def _auto():
            top.after(int((duration or 2.5) * 1000), _close)
        # schedule auto close
        try:
            _auto()
        except Exception:
            pass

    # center on parent
    try:
        parent.update_idletasks()
        w = top.winfo_reqwidth()
        h = top.winfo_reqheight()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        x = px + max(0, (pw - w) // 2)
        y = py + max(0, (ph - h) // 2)
        top.geometry(f"+{x}+{y}")
    except Exception:
        pass

    return dismissed
