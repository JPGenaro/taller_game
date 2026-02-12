import os
import shutil
import subprocess

class SoundManager:
    """Safe sound player with multiple fallbacks.

    Order of attempts:
    - `simpleaudio` (if available) with real volume control
    - system players `aplay` or `paplay` via subprocess (no per-play volume control)
    - no-op (silently ignore)
    """
    def __init__(self, assets_dir=None):
        self.assets_dir = assets_dir or os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "assets")
        self._player = None
        self._sa = None
        # try simpleaudio
        try:
            import simpleaudio as sa
            self._sa = sa
            self._player = "simpleaudio"
        except Exception:
            self._sa = None
            # try system players
            if shutil.which("paplay"):
                self._player = "paplay"
            elif shutil.which("aplay"):
                self._player = "aplay"
            else:
                self._player = None

        self.volume = 1.0
        self.muted = False

    def _fullpath(self, filename):
        return os.path.join(self.assets_dir, filename)

    def play(self, filename: str) -> bool:
        if self.muted or self.volume <= 0.0:
            return False
        path = self._fullpath(filename)
        if not os.path.exists(path):
            return False

        try:
            if self._player == "simpleaudio" and self._sa is not None:
                # simpleaudio: try to play with volume scaling if wav is 16-bit
                try:
                    import wave as _wave
                    from array import array
                    wf = _wave.open(path, 'rb')
                    sampwidth = wf.getsampwidth()
                    nchan = wf.getnchannels()
                    framerate = wf.getframerate()
                    frames = wf.readframes(wf.getnframes())
                    wf.close()
                    if sampwidth == 2 and self.volume != 1.0:
                        arr = array('h')
                        arr.frombytes(frames)
                        factor = float(self.volume)
                        for i in range(len(arr)):
                            v = int(arr[i] * factor)
                            if v > 32767: v = 32767
                            if v < -32768: v = -32768
                            arr[i] = v
                        play_obj = self._sa.play_buffer(arr.tobytes(), nchan, sampwidth, framerate)
                    else:
                        wave_obj = self._sa.WaveObject.from_wave_file(path)
                        wave_obj.play()
                    return True
                except Exception:
                    # fallback to simple play
                    try:
                        wave_obj = self._sa.WaveObject.from_wave_file(path)
                        wave_obj.play()
                        return True
                    except Exception:
                        return False

            elif self._player in ("aplay", "paplay"):
                try:
                    subprocess.Popen([self._player, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True
                except Exception:
                    return False

            else:
                # no available player -> silent fallback
                return False
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
