import numpy as np
from bg_utils import lfo_sine, SR

def process(x, *, state, f: float = 0.1, depth: float = 0.5, bias: float = 0.5, **_):
    n = x.shape[0]
    env = bias + depth * lfo_sine(n, float(f))
    return (x * env.astype(np.float32)).astype(np.float32)
