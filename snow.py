# snow.py
import numpy as np
from bg_utils import SR, pinkish, one_pole_lowpass, lfo_sine, stereo_normalize, stereo_from_mono

def generate_snow(duration_sec: int, level: float = 0.15, seed: int | None = None):
    n = int(duration_sec * SR)
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n, dtype=np.float32)
    base = pinkish(base)
    base = one_pole_lowpass(base, 1500.0)  # نطبّخ الهآيس
    base = one_pole_lowpass(base, 1200.0)

    # تغيّر طفيف وبطيء جدًا
    env = 0.9 + 0.1 * lfo_sine(n, 0.05, depth=1.0, phase=0.3)
    mono = base * env.astype(np.float32)
    st = stereo_from_mono(mono, spread=0.015, rng=rng)
    return stereo_normalize(st, level)
