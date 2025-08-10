from bg_utils import one_pole_lowpass
import numpy as np

def process(x, *, state, cut: float = 1000.0, gain: float = 1.0, **_):
    # HP بسيط: X - LP(X)
    hp = x - one_pole_lowpass(x, float(cut))
    return x + hp.astype(np.float32) * float(gain)
