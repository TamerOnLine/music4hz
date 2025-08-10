import numpy as np
from bg_utils import one_pole_lowpass

def process(x, *, state, lo: float = 200.0, hi: float = 1500.0, gain: float = 1.0, **_):
    bp = one_pole_lowpass(x, float(hi)) - one_pole_lowpass(x, float(lo))
    return (x + bp * float(gain)).astype(np.float32)
