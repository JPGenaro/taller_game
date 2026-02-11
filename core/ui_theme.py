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
    # Intentar cargar background si existe, usando CTkImage (evita advertencia HighDPI)
    try:
        from PIL import Image
        import os
        if root is not None:
            ruta = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "assets", "background.png")
            if os.path.exists(ruta):
                orig = Image.open(ruta).convert("RGBA")

                # create CTkImage slightly larger than window to allow parallax movement
                SCALE = 1.08

                def _create_bg(w, h):
                    try:
                        iw = max(1, int(w * SCALE))
                        ih = max(1, int(h * SCALE))
                        img_resized = orig.resize((iw, ih), Image.LANCZOS)
                        ctk_img = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=(iw, ih))
                        return ctk_img, iw, ih
                    except Exception:
                        return None, w, h

                # create initial image sized to current root or screen
                try:
                    w = root.winfo_width() if root.winfo_width() > 1 else root.winfo_screenwidth()
                    h = root.winfo_height() if root.winfo_height() > 1 else root.winfo_screenheight()
                except Exception:
                    w, h = root.winfo_screenwidth(), root.winfo_screenheight()

                bg_ctkimg, iw, ih = _create_bg(w, h)
                if bg_ctkimg:
                    root._bg_image = bg_ctkimg
                    # place image centered and slightly larger than window
                    lbl = ctk.CTkLabel(root, image=root._bg_image, text="")
                    x = int((w - iw) / 2)
                    y = int((h - ih) / 2)
                    lbl.place(x=x, y=y, width=iw, height=ih)
                    try:
                        lbl.lower()  # ensure background is behind everything
                    except Exception:
                        pass
                    root._bg_label = lbl

                    # debounce handler
                    def _on_resize(event):
                        # cancel pending
                        try:
                            if getattr(root, '_bg_after_id', None):
                                root.after_cancel(root._bg_after_id)
                        except Exception:
                            pass

                        def _do_resize():
                            try:
                                nw = max(1, root.winfo_width())
                                nh = max(1, root.winfo_height())
                                new_img, niw, nih = _create_bg(nw, nh)
                                if new_img:
                                    root._bg_image = new_img
                                    # update size and reposition to center
                                    x = int((nw - niw) / 2)
                                    y = int((nh - nih) / 2)
                                    root._bg_label.configure(image=root._bg_image)
                                    root._bg_label.place(x=x, y=y, width=niw, height=nih)
                                    root._bg_label.lower()
                            except Exception:
                                pass

                        root._bg_after_id = root.after(120, _do_resize)

                    # parallax on mouse move
                    MAX_OFFSET = 30

                    def _on_move(event):
                        try:
                            rw = max(1, root.winfo_width())
                            rh = max(1, root.winfo_height())
                            mx = event.x
                            my = event.y
                            rx = (mx / rw) - 0.5
                            ry = (my / rh) - 0.5
                            ox = int(-rx * MAX_OFFSET)
                            oy = int(-ry * MAX_OFFSET)
                            # current bg label size
                            bw = root._bg_label.winfo_width()
                            bh = root._bg_label.winfo_height()
                            x = int((rw - bw) / 2) + ox
                            y = int((rh - bh) / 2) + oy
                            root._bg_label.place(x=x, y=y)
                            root._bg_label.lower()
                        except Exception:
                            pass

                    try:
                        root.bind('<Motion>', _on_move)
                    except Exception:
                        pass

                    # bind configure
                    try:
                        root.bind('<Configure>', _on_resize)
                    except Exception:
                        pass
    except Exception:
        pass
    return True
