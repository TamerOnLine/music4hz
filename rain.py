import argparse
import os
import wave
import mimetypes
from typing import Tuple
import numpy as np

# --- simple rain synth -------------------------------------------------
def _one_pole_lowpass(x: np.ndarray, sr: int, cutoff_hz: float) -> np.ndarray:
    # y[n] = a*y[n-1] + (1-a)*x[n],  a ~ exp(-2*pi*fc/sr)
    a = np.exp(-2.0 * np.pi * cutoff_hz / sr, dtype=np.float32)
    y = np.empty_like(x)
    acc = np.float32(0.0)
    for i in range(x.shape[0]):
        acc = a * acc + (1.0 - a) * x[i]
        y[i] = acc
    return y

def _pinkish(x: np.ndarray) -> np.ndarray:
    # خلط 3 مرّات Lowpass خفيفة لإحساس 1/f بسيط
    x = _one_pole_lowpass(x, sr=44100, cutoff_hz=8000.0)
    x = _one_pole_lowpass(x, sr=44100, cutoff_hz=4000.0)
    x = _one_pole_lowpass(x, sr=44100, cutoff_hz=2000.0)
    return x

def generate_rain(duration_sec: int, sr: int, level: float = 0.25) -> np.ndarray:
    """
    توليد مطر ستيريو: ضجيج مُفلتر + تذبذب بطيء في الشدة.
    level: 0..1 شدة المطر.
    """
    n = int(duration_sec * sr)
    rng = np.random.default_rng()
    # ضجيج أبيض لقناتين مع اختلاف بسيط
    left = rng.standard_normal(n, dtype=np.float32)
    right = rng.standard_normal(n, dtype=np.float32) * 0.97 + rng.standard_normal(n, dtype=np.float32) * 0.03

    # نخففه ونخلي لونه وردي/ناعم
    left = _pinkish(left)
    right = _pinkish(right)

    # تذبذب بطيء (0.1..0.3 Hz) + تموج أسرع (1..3 Hz) لتغيّر المطر
    t = np.arange(n, dtype=np.float32) / np.float32(sr)
    slow_rate = 0.1 + 0.2 * rng.random()
    fast_rate = 1.0 + 2.0 * rng.random()
    env = (0.7 + 0.3 * np.sin(2*np.pi*slow_rate*t).astype(np.float32)) * (0.8 + 0.2 * np.sin(2*np.pi*fast_rate*t + 1.1).astype(np.float32))

    left *= env
    right *= env * 0.98  # فرق بسيط

    # Normalize خفيف ثم تطبيق المستوى المطلوب
    mix = np.stack([left, right], axis=1)
    peak = np.max(np.abs(mix)) + 1e-7
    mix = (mix / peak) * np.float32(level)
    return mix
