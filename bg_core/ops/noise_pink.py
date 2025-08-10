import numpy as np
from bg_utils import pinkish

def process(x, *, state, gain: float = 1.0, **_):
    n = x.shape[0]
    rng = np.random.default_rng(state.get("seed"))
    base = pinkish(rng.standard_normal(n, dtype=np.float32))
    return (x + base * float(gain)).astype(np.float32)
