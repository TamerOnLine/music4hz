# trees.py
import numpy as np
from bg_utils import SR, pinkish, one_pole_lowpass, stereo_normalize

def generate_trees(duration_sec: int, level: float = 0.2, seed: int | None = None):
    n = int(duration_sec * SR)
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n, dtype=np.float32)
    base = pinkish(base)

    # نرفع النطاق المتوسط-العالي: فلترين وتسوية
    hi = base - one_pole_lowpass(base, 1200.0)
    hi = one_pole_lowpass(hi, 4000.0)

    # دفعات قصيرة (rustle bursts)
    bursts = np.zeros(n, dtype=np.float32)
    num = max(8, int(duration_sec // 5))
    for _ in range(num):
        pos = rng.integers(0, max(1, n- SR//2))
        length = rng.integers(SR//16, SR//6)  # 60..250 ms تقريبًا
        amp = rng.uniform(0.2, 0.6)
        bursts[pos:pos+length] += amp

    bursts = one_pole_lowpass(bursts, 60.0)
    mono = (0.6 * hi + 0.4 * base) * (0.7 + bursts)
    left = mono
    right = mono * 0.97 + rng.standard_normal(n, dtype=np.float32) * 0.01
    st = np.stack([left, right], axis=1)
    return stereo_normalize(st, level)
