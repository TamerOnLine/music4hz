import numpy as np
from bg_utils import one_pole_lowpass

def process(x, *, state, cut: float = 1000.0, gain: float = 1.0, **_):
    return (x + one_pole_lowpass(x, float(cut)) * float(gain)).astype(np.float32)
