import os

class SoundManager:
    """Reproduce sonidos WAV si la dependencia y el archivo existen.
    Uso seguro: si no existe simpleaudio o el archivo, no lanza excepción, solo hace fallback.
    """
    def __init__(self, assets_dir=None):
        self.assets_dir = assets_dir or os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "assets")
        self._enabled = False
        self._sa = None
        try:
            import simpleaudio as sa
            self._sa = sa
            self._enabled = True
        except Exception:
            self._enabled = False
        # defaults
        self.volume = 1.0
        self.muted = False

    def _fullpath(self, filename):
        return os.path.join(self.assets_dir, filename)

    def play(self, filename):
        if not self._enabled:
            return False
        if self.muted or self.volume <= 0.0:
            return False
        path = self._fullpath(filename)
        if not os.path.exists(path):
            return False
        try:
            # Read raw frames and scale by volume
            import wave as _wave
            from array import array
            wf = _wave.open(path, 'rb')
            nchan = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            frames = wf.readframes(nframes)
            wf.close()

            if sampwidth != 2:
                # fallback to simple play
                wave_obj = self._sa.WaveObject.from_wave_file(path)
                wave_obj.play()
                return True

            # 16-bit samples
            arr = array('h')
            arr.frombytes(frames)
            # scale samples
            if self.volume != 1.0:
                factor = float(self.volume)
                for i in range(len(arr)):
                    v = int(arr[i] * factor)
                    if v > 32767: v = 32767
                    if v < -32768: v = -32768
                    arr[i] = v

            # play buffer
            play_obj = self._sa.play_buffer(arr.tobytes(), nchan, sampwidth, framerate)
            return True
        except Exception:
            return False

    def set_volume(self, value: float):
        self.volume = max(0.0, min(1.0, float(value)))

    def set_muted(self, muted: bool):
        self.muted = bool(muted)

# Singleton
_sound_manager = None

def get_sound_manager():
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
