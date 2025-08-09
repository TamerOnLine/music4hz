# theta_4hz_generator.py
import numpy as np, wave

def save_wav(path, data, sr=44100):
    data_i16 = (np.clip(data, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(data.shape[1])
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data_i16.tobytes())

def make(theta_hz=4.0, duration_sec=600, sr=44100,
         binaural_carriers=(220.0, 224.0), iso_carrier=400.0, amp=0.3):
    t = np.linspace(0, duration_sec, int(sr*duration_sec), endpoint=False)
    # فِيد داخلي/خارجي نصف ثانية لتجنّب نقرات
    fade = int(sr*0.5)
    env = np.ones_like(t)
    env[:fade] = np.linspace(0,1,fade)
    env[-fade:] = np.linspace(1,0,fade)

    # Binaural (سماعات)
    l, r = binaural_carriers
    left  = env * amp * np.sin(2*np.pi*l*t)
    right = env * amp * np.sin(2*np.pi*r*t)
    binaural = np.stack([left, right], axis=1)

    # Isochronic (سماعات خارجية)
    am = env * (0.5 * (1 + np.sin(2*np.pi*theta_hz*t)))
    iso = am * amp * np.sin(2*np.pi*iso_carrier*t)
    isochronic = np.stack([iso, iso], axis=1)
    return binaural, isochronic, sr

if __name__ == "__main__":
    duration_minutes = 10  # عدّلها كما تريد
    binaural, iso, sr = make(duration_sec=duration_minutes*60)
    save_wav("theta_4hz_binaural.wav", binaural, sr)
    save_wav("theta_4hz_iso.wav", iso, sr)
    print("Saved: theta_4hz_binaural.wav, theta_4hz_iso.wav")
