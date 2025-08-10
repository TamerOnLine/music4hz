"""
bg_utils.py — أدوات مساعدة لتوليد ومعالجة الإشارات الصوتية
"""

import numpy as np

# 🎯 معدل العينة الافتراضي (Hz)
SR = 44100


# ─────────────────────────────
# 📌 توليد الضوضاء والموجات البطيئة
# ─────────────────────────────

def pinkish(white: np.ndarray) -> np.ndarray:
    """
    تحويل ضوضاء بيضاء إلى ضوضاء وردية باستخدام خوارزمية فلتر بسيطة.
    white: مصفوفة ضوضاء بيضاء (float32)
    """
    b = np.zeros(7, dtype=np.float32)
    pink = np.zeros_like(white)
    for i, w in enumerate(white):
        b[0] = 0.99886 * b[0] + w * 0.0555179
        b[1] = 0.99332 * b[1] + w * 0.0750759
        b[2] = 0.96900 * b[2] + w * 0.1538520
        b[3] = 0.86650 * b[3] + w * 0.3104856
        b[4] = 0.55000 * b[4] + w * 0.5329522
        b[5] = -0.7616 * b[5] - w * 0.0168980
        pink[i] = b[0] + b[1] + b[2] + b[3] + b[4] + b[5] + b[6] + w * 0.5362
        b[6] = w * 0.115926
    return pink.astype(np.float32)


def lfo_sine(n: int, f: float) -> np.ndarray:
    """
    توليد موجة LFO جيبية.
    n: عدد العينات
    f: تردد LFO (Hz)
    """
    t = np.arange(n, dtype=np.float32) / np.float32(SR)
    return np.sin(2 * np.pi * np.float32(f) * t)


# ─────────────────────────────
# 📌 فلاتر بسيطة
# ─────────────────────────────

def one_pole_lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """
    فلتر Low-Pass من رتبة أولى.
    cutoff: التردد القاطع (Hz)
    """
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = (1 - a) * x[i] + a * y[i - 1]
    return y.astype(np.float32)


def one_pole_highpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """
    فلتر High-Pass من رتبة أولى.
    cutoff: التردد القاطع (Hz)
    """
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = a * (y[i - 1] + x[i] - x[i - 1])
    return y.astype(np.float32)


# ─────────────────────────────
# 📌 معالجة ستيريو
# ─────────────────────────────

def stereo_normalize(x: np.ndarray, target_level: float = 0.2) -> np.ndarray:
    """
    موازنة مستوى إشارة ستيريو للوصول إلى target_level.
    """
    peak = np.max(np.abs(x))
    if peak == 0:
        return x
    return (x / peak * target_level).astype(np.float32)
