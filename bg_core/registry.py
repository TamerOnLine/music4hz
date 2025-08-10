# bg_core/registry.py
from importlib import import_module

_OPS = {
    "noise_pink":   "bg_core.ops.noise_pink",
    "filter_lp":    "bg_core.ops.filter_lp",
    "filter_hp":    "bg_core.ops.filter_hp",
    "filter_bp":    "bg_core.ops.filter_bp",
    "env_lfo":      "bg_core.ops.env_lfo",
    "bursts":       "bg_core.ops.bursts",
    "stereo_decor": "bg_core.ops.stereo_decor",
}

_CACHE = {}

def get_op(name: str):
    """Return operator callable: process(x, *, state, **kwargs) -> np.ndarray"""
    if name in _CACHE:
        return _CACHE[name]
    if name not in _OPS:
        raise KeyError(f"Unknown operator '{name}'. Known: {', '.join(sorted(_OPS))}")
    mod = import_module(_OPS[name])
    fn = getattr(mod, "process")
    _CACHE[name] = fn
    return fn
