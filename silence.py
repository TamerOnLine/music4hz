# silence.py
import numpy as np
from bg_utils import SR

def generate_silence(duration_sec: int, level: float = 0.0, seed: int | None = None):
    n = int(duration_sec * SR)
    return np.zeros((n, 2), dtype=np.float32)
