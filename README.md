Garage Tycoon - Assets & Run

Este proyecto usa imágenes y sonidos opcionales para mejorar la UI. Si no colocás los archivos, la app funciona igual pero sin imágenes/sonidos.

Assets (colocar en `assets/`):
- `background.png` — imagen de fondo para la ventana principal (recomendado 1000x700 o tamaño grande).
- `icon_buy.png` — icono pequeño para botones de compra.
- `sound_buy.wav` — efecto de sonido para comprar.
- `sound_repair.wav` — efecto de sonido para reparar.
- `sound_sell.wav` — efecto de sonido para vender.

Instalación de dependencias (virtualenv recomendado):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ejecutar tests:

```bash
python -m unittest discover -s tests
```

Ejecutar la app:

```bash
python main.py
```

Notas:
- Los sonidos son opcionales; si faltan, la app seguirá funcionando.
- Para un estilo más pulido, podés reemplazar `assets/background.png` y los íconos.
