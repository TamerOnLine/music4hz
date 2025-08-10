import numpy as np
from bg_utils import SR, one_pole_lowpass

def process(x, *, state, density: float = 20.0, min_ms: float = 40.0, max_ms: float = 200.0,
            amp_lo: float = 0.2, amp_hi: float = 0.6, gain: float = 1.0, **_):
    n = x.shape[0]
    rng = np.random.default_rng(state.get("seed"))
    out = np.zeros(n, dtype=np.float32)
    total = int(density * (n / SR) / 60.0)
    for _ in range(max(0, total)):
        pos = rng.integers(0, max(1, n - SR // 5))
        L = rng.integers(int(SR * (min_ms / 1000.0)), int(SR * (max_ms / 1000.0)))
        amp = rng.uniform(amp_lo, amp_hi)
        out[pos:pos+L] += amp * np.linspace(1.0, 0.0, L, dtype=np.float32)
    # تمييز “النقر” بإزالة المنخفضات قليلاً
    out = out - one_pole_lowpass(out, 2000.0)
    return x + out * float(gain)
