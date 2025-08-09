# app.py
import argparse, numpy as np, wave, os

def save_wav(path, data, sr=44100):
    data_i16 = (np.clip(data, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(data.shape[1])
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data_i16.tobytes())

def make(theta_hz=4.0, duration_sec=600, sr=44100,
         binaural_carriers=(220.0, 224.0), iso_carrier=400.0, amp=0.3):
    # استخدم float32 لتقليل الذاكرة
    t = np.linspace(0, duration_sec, int(sr*duration_sec), endpoint=False, dtype=np.float32)

    fade = int(sr*0.5)
    env = np.ones_like(t, dtype=np.float32)
    env[:fade] = np.linspace(0, 1, fade, dtype=np.float32)
    env[-fade:] = np.linspace(1, 0, fade, dtype=np.float32)

    # Binaural
    l, r = binaural_carriers
    left  = env * amp * np.sin(2*np.pi*l*t, dtype=np.float32)
    right = env * amp * np.sin(2*np.pi*r*t, dtype=np.float32)
    binaural = np.stack([left, right], axis=1)

    # Isochronic (AM ناعمة؛ إن أردت نبضات مربعة استخدم بوابة duty cycle)
    am = env * (0.5 * (1 + np.sin(2*np.pi*theta_hz*t, dtype=np.float32)))
    iso = am * amp * np.sin(2*np.pi*iso_carrier*t, dtype=np.float32)
    isochronic = np.stack([iso, iso], axis=1)
    return binaural, isochronic, sr

def main():
    p = argparse.ArgumentParser(description="Generate 4Hz theta tones (binaural/isochronic)")
    p.add_argument("--mode", choices=["binaural","iso","both"], default="both")
    p.add_argument("--minutes", type=float, default=10.0)
    p.add_argument("--theta", type=float, default=4.0)
    p.add_argument("--amp", type=float, default=0.3)
    p.add_argument("--binaural", type=float, nargs=2, metavar=("L","R"), default=(220.0,224.0))
    p.add_argument("--iso-carrier", type=float, default=400.0)
    p.add_argument("--sr", type=int, default=44100)
    p.add_argument("--out", default=".")
    args = p.parse_args()

    dur = int(args.minutes*60)
    binaural, iso, sr = make(theta_hz=args.theta, duration_sec=dur, sr=args.sr,
                             binaural_carriers=tuple(args.binaural),
                             iso_carrier=args.iso_carrier, amp=args.amp)

    os.makedirs(args.out, exist_ok=True)
    if args.mode in ("binaural","both"):
        save_wav(os.path.join(args.out, f"theta_{args.theta:g}hz_binaural.wav"), binaural, sr)
    if args.mode in ("iso","both"):
        save_wav(os.path.join(args.out, f"theta_{args.theta:g}hz_iso.wav"), iso, sr)
    print("Done.")

if __name__ == "__main__":
    main()
