# 🎵 music4hz — Brainwave Entrainment Audio Generator (Binaural & Isochronic)

![Build](https://github.com/TamerOnLine/pro_venv/actions/workflows/test-pro_venv.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/TamerOnLine/pro_venv?style=flat-square)
![License](https://img.shields.io/github/license/TamerOnLine/pro_venv?style=flat-square)


## 📌 Overview
The **music4hz** project provides a flexible tool to generate WAV files containing **brainwave entrainment** audio using:
- **Binaural Beats** — different frequency in each ear to create a perceived frequency difference in the brain.
- **Isochronic Tones** — single tone modulated on and off at a target frequency.

Supports generating audio for multiple brainwave bands (Delta, Theta, Alpha, Beta, Gamma) with full control over duration, amplitude, and carrier frequencies.

---

## ✨ Features
- Generate **Binaural** and **Isochronic** tones in 16-bit PCM.
- Supports **multiple brainwave bands** with default durations for each.
- Control:
  - Beat frequency (Hz)
  - Duration (minutes)
  - Amplitude
  - Carrier frequencies
  - Sample rate
- Batch generation via `make-tones.py` for all bands.
- Cross-platform support (Windows / Linux / macOS).

---

## 📂 Project Structure
```
music4hz/
├── app.py              # Main generator for binaural/isochronic
├── make-tones.py       # Batch generator for all bands
├── pro_venv.py         # Portable environment setup tool
├── main.py             # Safe launcher inside venv
├── requirements.txt    # Dependencies (numpy)
├── setup-config.json   # Project settings
└── out/                # Output directory for generated audio
```

---

## 🚀 Quick Start
### 1) First run
```bash
python pro_venv.py
```

### 2) Generate a Theta 4 Hz tone for 30 minutes:
```bash
python app.py --mode both --theta 4 --minutes 30 --out out/theta
```

### 3) Generate all bands at once:
```bash
python make-tones.py
```

---

## 📊 Brainwave Bands and Studies
| Band | Frequency (Hz) | Suggested Duration (min) | Common Use | Studies |
|------|---------------|--------------------------|------------|---------|
| **Delta** | 1–3 | 90 | Deep sleep, body repair | [Boutin et al., 2018](https://doi.org/10.3389/fnins.2018.00238) |
| **Theta** | 4–7 | 45 | Relaxation, daydreaming, creativity | [Kasprzak, 2011](https://doi.org/10.2478/v10068-011-0005-1) |
| **Alpha** | 8–12 | 30 | Light focus, relaxed alertness | [Jirakittayakorn & Wongsawat, 2017](https://doi.org/10.3389/fnins.2017.00254) |
| **Beta** | 18 | 20 | Alertness, high concentration, problem-solving | [Lane et al., 1998](https://doi.org/10.1016/S0301-0511(98)00028-8) |
| **Gamma** | 40 | 15 | Working memory, cognitive processing | [Herrmann et al., 2016](https://doi.org/10.1016/j.tics.2016.01.003) |
| **Super Gamma** | 110, 120, 136.1, 150, 200 | 10–15 |  
110 Hz – Deep meditation / creativity  
120 Hz – Expanded awareness  
136.1 Hz – "OM frequency" (spiritual traditions)  
150 Hz – High attention (TMS research)  
200 Hz – Ultra neural activity | [Lutz et al., 2004](https://doi.org/10.1073/pnas.0407401101) |


> **Note:** Results may vary between individuals; this project is not a substitute for medical advice.

---

## ⚙️ CLI Options (`app.py`)
| Option | Description | Default |
|--------|-------------|---------|
| `--mode` | Generation mode: `binaural` / `iso` / `both` | `both` |
| `--minutes` | Signal duration in minutes | `30` |
| `--theta` | Beat frequency (Hz) | `4.0` |
| `--amp` | Amplitude [0–1] | `0.3` |
| `--binaural` | Left & right carrier frequencies (Hz) | `220.0 224.0` |
| `--iso-carrier` | Carrier frequency for isochronic tone | `400.0` |
| `--sr` | Sample rate (Hz) | `44100` |
| `--out` | Output directory | `.` |

---

## 📜 License
MIT — See `LICENSE`.
