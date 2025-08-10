from bg_utils import one_pole_lowpass
import numpy as np

def process(x, *, state, lo: float = 200.0, hi: float = 1500.0, gain: float = 1.0, **_):
    # BP بسيط: LP(high) - LP(low)
    bp = one_pole_lowpass(x, float(hi)) - one_pole_lowpass(x, float(lo))
    return x + bp.astype(np.float32) * float(gain)
