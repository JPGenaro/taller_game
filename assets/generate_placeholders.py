from PIL import Image, ImageDraw, ImageFont
import wave
import math
import struct
import os

OUT_DIR = os.path.join(os.path.dirname(__file__))

# Create background.png
bg_path = os.path.join(OUT_DIR, 'background.png')
if not os.path.exists(bg_path):
    w, h = 1200, 900
    img = Image.new('RGB', (w, h), (18, 24, 34))
    draw = ImageDraw.Draw(img)
    # simple gradient
    for i in range(h):
        r = int(18 + (i / h) * 20)
        g = int(24 + (i / h) * 30)
        b = int(34 + (i / h) * 40)
        draw.line([(0, i), (w, i)], fill=(r, g, b))
    # text
    try:
        f = ImageFont.truetype('DejaVuSans-Bold.ttf', 72)
    except Exception:
        f = ImageFont.load_default()
    draw.text((40, 40), 'GARAGE TYCOON', font=f, fill=(240, 240, 240))
    img.save(bg_path)
    print('Wrote', bg_path)
else:
    print('Exists', bg_path)

# Create icon_buy.png
icon_path = os.path.join(OUT_DIR, 'icon_buy.png')
if not os.path.exists(icon_path):
    size = (128, 128)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([16, 48, 112, 96], fill=(60, 180, 90))
    draw.polygon([(96, 48), (112, 32), (112, 48)], fill=(40, 160, 70))
    img.save(icon_path)
    print('Wrote', icon_path)
else:
    print('Exists', icon_path)

# Create simple WAVs: buy, repair, sell

def make_sine(path, freq=440.0, duration=0.25, volume=0.3, samplerate=44100):
    nframes = int(samplerate * duration)
    amplitude = int(32767 * volume)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        for i in range(nframes):
            t = float(i) / samplerate
            v = int(amplitude * math.sin(2.0 * math.pi * freq * t))
            data = struct.pack('<h', v)
            wf.writeframesraw(data)
    print('Wrote', path)

buy_wav = os.path.join(OUT_DIR, 'sound_buy.wav')
repair_wav = os.path.join(OUT_DIR, 'sound_repair.wav')
sell_wav = os.path.join(OUT_DIR, 'sound_sell.wav')

if not os.path.exists(buy_wav):
    make_sine(buy_wav, freq=880.0, duration=0.15, volume=0.5)
else:
    print('Exists', buy_wav)

if not os.path.exists(repair_wav):
    make_sine(repair_wav, freq=440.0, duration=0.35, volume=0.4)
else:
    print('Exists', repair_wav)

if not os.path.exists(sell_wav):
    make_sine(sell_wav, freq=660.0, duration=0.2, volume=0.45)
else:
    print('Exists', sell_wav)
