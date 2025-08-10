# wind.py
import numpy as np
from bg_utils import SR, pinkish, one_pole_lowpass, lfo_sine, stereo_normalize, stereo_from_mono

def generate_wind(duration_sec: int, level: float = 0.25, seed: int | None = None):
    n = int(duration_sec * SR)
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n, dtype=np.float32)
    base = pinkish(base)
    # نعمل Band-limit: Lowpass قوي ثم نطرح Lowpass أبطأ لنعطي نطاق متوسط
    low = one_pole_lowpass(base, 300.0)
    very_low = one_pole_lowpass(base, 60.0)
    band = low - 0.6 * very_low

    # هبوب (Gusts): LFO بطيء + LFO أبطأ جدًا
    env = 0.6 + 0.4 * lfo_sine(n, 0.08, depth=1.0, phase=0.0)
    env *= 0.8 + 0.2 * lfo_sine(n, 0.015, depth=1.0, phase=0.7)

    mono = band * env.astype(np.float32)
    # ستيريو مع اختلاف بسيط
    st = stereo_from_mono(mono, spread=0.03, rng=rng)
    return stereo_normalize(st, level)
