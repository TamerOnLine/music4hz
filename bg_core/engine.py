# bg_core/engine.py
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from bg_utils import SR, stereo_normalize
from .registry import get_op

def _parse_step(step: str):
    # "op:arg1=val1,arg2=val2" -> ("op", {"arg1":val1,...})
    if ":" not in step:
        return step.strip(), {}
    name, argstr = step.split(":", 1)
    args = {}
    for p in argstr.split(","):
        if not p:
            continue
        k, v = p.split("=")
        try:
            args[k] = float(v)
        except ValueError:
            args[k] = v
    return name.strip(), args

def run_profile(profile_path: str, minutes: float, *, seed: int | None = None, level: float | None = None):
    """Load JSON profile and run its pipeline -> return stereo float32 @ SR."""
    cfg = json.loads(Path(profile_path).read_text(encoding="utf-8"))
    steps = cfg.get("pipeline", [])
    target = float(cfg.get("level", 0.2)) if level is None else float(level)

    n = int(minutes * 60 * SR)
    x = np.zeros(n, dtype=np.float32)
    state = {"SR": SR, "seed": seed}

    for step in steps:
        name, kwargs = _parse_step(step)
        op = get_op(name)
        x = op(x, state=state, **kwargs)

    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    return stereo_normalize(x, target)
