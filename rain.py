# rain.py
import numpy as np
from bg_utils import SR, pinkish, lfo_sine, stereo_normalize, stereo_from_mono

def generate_rain(duration_sec: int, level: float = 0.25, seed: int | None = None):
    n = int(duration_sec * SR)
    rng = np.random.default_rng(seed)
    left = rng.standard_normal(n, dtype=np.float32)
    right = rng.standard_normal(n, dtype=np.float32) * 0.97 + rng.standard_normal(n, dtype=np.float32) * 0.03
    left = pinkish(left); right = pinkish(right)

    t = np.arange(n, dtype=np.float32) / np.float32(SR)
    slow = 0.1 + 0.2 * (rng.random())
    fast = 1.0 + 2.0 * (rng.random())
    env = (0.7 + 0.3 * np.sin(2*np.pi*slow*t).astype(np.float32)) * (0.8 + 0.2 * np.sin(2*np.pi*fast*t + 1.1).astype(np.float32))

    mix = np.stack([left * env, right * env * 0.98], axis=1)
    return stereo_normalize(mix, level)
