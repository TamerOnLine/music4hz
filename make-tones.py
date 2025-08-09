import sys
import subprocess
from pathlib import Path

# ===== Settings =====

python_exe = Path(sys.executable).resolve()  
amp = 0.35
carrier = 400

minutes = {
    "delta": 90,
    "theta": 45,
    "alpha": 30,
    "beta": 20,
    "gamma": 15
}

sets = [
    {"band": "delta", "freqs": range(1, 4)},   # 1,2,3 Hz
    {"band": "theta", "freqs": range(4, 8)},   # 4..7 Hz
    {"band": "alpha", "freqs": range(8, 13)},  # 8..12 Hz
    {"band": "beta",  "freqs": [18]},          # 18 Hz
    {"band": "gamma", "freqs": [40]}           # 40 Hz
]

# ===== Execution =====
root = Path.cwd()
out_root = root / "out"
out_root.mkdir(exist_ok=True)

for s in sets:
    band = s["band"]
    band_out = out_root / band
    band_out.mkdir(exist_ok=True)
    for hz in s["freqs"]:
        name = f"{band}_{hz}hz_iso.wav"
        file_path = band_out / name

        if file_path.exists():
            print(f"!! Skipping {name} (already exists)")
            continue

        print(f">> Generating {name} ...")
        cmd = [
            str(python_exe), "app.py",
            "--mode", "iso",
            "--theta", str(hz),
            "--minutes", str(minutes[band]),
            "--amp", str(amp),
            "--iso-carrier", str(carrier),
            "--out", str(band_out)
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"!! Failed: {name}")
            break

print(f"\nDone. Files under: {out_root}")