# sea.py
import numpy as np
from bg_utils import SR, pinkish, one_pole_lowpass, lfo_sine, stereo_normalize

def generate_sea(duration_sec: int, level: float = 0.25, seed: int | None = None):
    n = int(duration_sec * SR)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n, dtype=np.float32)
    noise = pinkish(noise)
    # جسم الموج منخفض
    body = one_pole_lowpass(noise, 300.0)
    # رغوة أعلى قليلاً
    foam = one_pole_lowpass(noise, 1500.0) - one_pole_lowpass(noise, 500.0)

    # دورات موج 0.07..0.12 Hz + تموج ثانوي 0.3..0.5 Hz
    cycle = 0.07 + 0.05 * rng.random()
    sub = 0.3 + 0.2 * rng.random()
    env = (0.5 + 0.5 * lfo_sine(n, cycle, depth=1.0)) * (0.8 + 0.2 * lfo_sine(n, sub, depth=1.0, phase=0.6))

    left = (body * env + 0.30 * foam).astype(np.float32)
    right = (body * (env * 0.98) + 0.30 * foam * 0.97).astype(np.float32)
    st = np.stack([left, right], axis=1)
    return stereo_normalize(st, level)
