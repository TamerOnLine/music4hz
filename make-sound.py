import sys
import subprocess
from pathlib import Path

# ===== Settings =====

python_exe = Path(sys.executable).resolve()
amp = 0.35
carrier = 400

# Default durations per band (minutes)
minutes = {
    "delta": 90,
    "theta": 45,
    "alpha": 30,
    "beta": 20,
    "gamma": 15,
    "supergamma": 12,
}

# Which tracks to generate
sets = [
    {"band": "delta", "freqs": [0.5]},
    {"band": "delta", "freqs": range(1, 4)},      # 1..3 Hz
    {"band": "theta", "freqs": range(4, 8)},      # 4..7 Hz
    {"band": "alpha", "freqs": range(8, 13)},     # 8..12 Hz
    {"band": "beta",  "freqs": [18]},             # 18 Hz
    {"band": "gamma", "freqs": [40]},             # 40 Hz
    # Super Gamma range
    {"band": "supergamma", "freqs": [
        110,     # Deep meditation / creativity
        120,     # Expanded awareness
        136.1,   # OM frequency
        150,     # TMS high attention
        200      # Ultra neural activity
    ]},
]


# ----- Optional metadata (leave empty to skip) -----
artist = "TamerOnLine"
year = "2025"
copyright_text = "© 2025 TamerOnLine. All rights reserved."
email = "info@tameronline.com"
url = "https://tameronline.com"
artwork = ""  # e.g. r"E:\images\logo.png"
title_prefix = ""  # e.g. "music4hz"

# ===== Execution =====
root = Path.cwd()
out_root = root / "out"
out_root.mkdir(exist_ok=True)

def maybe_extend(cmd, flag, value):
    if value:
        cmd.extend([flag, str(value)])

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
            str(python_exe), "sound.py",
            "--mode", "iso",
            "--freq", str(hz),                    # <-- was --theta
            "--minutes", str(minutes[band]),
            "--amp", str(amp),
            "--iso-carrier", str(carrier),
            "--out", str(band_out),
        ]

        # Optional metadata
        maybe_extend(cmd, "--artist", artist)
        maybe_extend(cmd, "--year", year)
        maybe_extend(cmd, "--copyright", copyright_text)
        maybe_extend(cmd, "--email", email)
        maybe_extend(cmd, "--url", url)
        maybe_extend(cmd, "--artwork", artwork)
        maybe_extend(cmd, "--title-prefix", title_prefix)

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"!! Failed: {name}")
            break

print(f"\nDone. Files under: {out_root}")
