import numpy as np
from bg_utils import one_pole_lowpass, SR

def process(x, *, state, spread: float = 0.02, pan_rate: float = 0.01, pan_depth: float = 0.1, **_):
    if x.ndim == 2:
        return x.astype(np.float32)
    n = x.shape[0]
    rng = np.random.default_rng(state.get("seed"))
    decor = rng.standard_normal(n).astype(np.float32) * np.float32(spread)
    decor = one_pole_lowpass(decor, 1200.0)
    t = np.arange(n, dtype=np.float32) / np.float32(SR)
    pan = np.sin(2*np.pi*pan_rate*t + rng.uniform(0, 2*np.pi)).astype(np.float32) * np.float32(pan_depth)
    L = (x + 0.5*decor) * (1.0 + pan)
    R = (x - 0.5*decor) * (1.0 - pan)
    return np.stack([L, R], axis=1).astype(np.float32)
