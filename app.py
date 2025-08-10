"""Generate tones as binaural or isochronic audio and write WAV files.

This script synthesizes binaural and isochronic tones at a given beat frequency
and saves them as 16-bit PCM WAV files, embedding metadata (title, artist,
copyright, email, website, and optional artwork).
"""

import argparse
import os
import wave
import mimetypes
from typing import Tuple
import numpy as np


# --- WAV metadata via ID3-in-WAV (mutagen) ---
def set_wav_metadata(
    path: str,
    *,
    title: str = "",
    artist: str = "",
    comment: str = "",
    year: str = "",
    copyright_: str = "",
    url: str = "",
    email: str = "",
    artwork_path: str = "",
) -> bool:
    """Attach metadata (and optional artwork) to a WAV file. Non-fatal on failure."""
    try:
        from mutagen.wave import WAVE
        from mutagen.id3 import (
            ID3NoHeaderError,
            TIT2, TPE1, COMM, TDRC, TCOP, WOAF, APIC,
        )

        audio = WAVE(path)
        try:
            _ = audio.tags
            if audio.tags is None:
                audio.add_tags()
        except ID3NoHeaderError:
            audio.add_tags()

        # Clear frames we set
        for frame in ("TIT2", "TPE1", "COMM", "TDRC", "TCOP", "WOAF", "APIC"):
            audio.tags.delall(frame)

        # Build a visible comment (each item on its own line)
        parts = []
        if comment:
            parts.append(comment)
        if email:
            parts.append(f"Email: {email}")
        if url:
            parts.append(f"Website: {url}")
        comment_text = "\n".join(parts) if parts else ""

        if title:
            audio.tags.add(TIT2(encoding=3, text=title))
        if artist:
            audio.tags.add(TPE1(encoding=3, text=artist))
        if comment_text:
            audio.tags.add(COMM(encoding=3, lang="eng", desc="", text=comment_text))
        if year:
            audio.tags.add(TDRC(encoding=3, text=year))
        if copyright_:
            audio.tags.add(TCOP(encoding=3, text=copyright_))
        if url:
            audio.tags.add(WOAF(encoding=3, url=url))

        # Artwork (optional)
        if artwork_path and os.path.exists(artwork_path):
            try:
                mime, _ = mimetypes.guess_type(artwork_path)
                if mime is None:
                    ext = os.path.splitext(artwork_path)[1].lower()
                    mime = "image/png" if ext == ".png" else "image/jpeg"
                with open(artwork_path, "rb") as f:
                    img = f.read()
                audio.tags.add(
                    APIC(encoding=3, mime=mime, type=3, desc="Cover", data=img)
                )
            except Exception as e:
                print(f"[meta] Skipped artwork for {path}: {e}")

        audio.save()
        return True
    except Exception as e:
        print(f"[meta] Skipped metadata for {path}: {e}")
        return False


def save_wav(path: str, data: np.ndarray, sr: int = 44100) -> None:
    """Write a mono/stereo float array in [-1, 1] to a 16-bit WAV file."""
    if data.ndim == 1:
        data = data[:, None]
    data_i16 = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(data_i16.shape[1])
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sr)
        wf.writeframes(data_i16.tobytes())


def make(
    beat_hz: float,
    duration_sec: int = 600,
    sr: int = 44100,
    binaural_carriers: Tuple[float, float] = (220.0, 224.0),
    iso_carrier: float = 400.0,
    amp: float = 0.3,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """Generate binaural and isochronic tones at the given beat frequency."""
    n = int(sr * duration_sec)
    t = np.arange(n, dtype=np.float32) / np.float32(sr)

    # 0.5 s fade in/out
    fade = int(sr * 0.5)
    env = np.ones_like(t, dtype=np.float32)
    if fade > 0 and fade * 2 < n:
        env[:fade] = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        env[-fade:] = np.linspace(1.0, 0.0, fade, dtype=np.float32)

    two_pi = np.float32(2.0 * np.pi)
    l32, r32 = map(np.float32, binaural_carriers)
    beat32 = np.float32(beat_hz)
    iso_c32 = np.float32(iso_carrier)
    amp32 = np.float32(amp)

    # Binaural: L/R carriers
    left = env * amp32 * np.sin(two_pi * l32 * t)
    right = env * amp32 * np.sin(two_pi * r32 * t)
    binaural = np.stack([left, right], axis=1)

    # Isochronic: AM at beat_hz on carrier
    am = env * (np.float32(0.5) * (np.float32(1.0) + np.sin(two_pi * beat32 * t)))
    iso = am * amp32 * np.sin(two_pi * iso_c32 * t)
    isochronic = np.stack([iso, iso], axis=1)

    return binaural, isochronic, sr


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate tones (binaural / isochronic) with embedded metadata."
    )
    parser.add_argument("--mode", choices=["binaural", "iso", "both"], default="both")
    parser.add_argument("--minutes", type=float, default=30.0)
    parser.add_argument("--freq", type=float, default=4.0, help="Beat frequency (Hz).")
    parser.add_argument("--amp", type=float, default=0.3)
    parser.add_argument(
        "--binaural", type=float, nargs=2, metavar=("L", "R"), default=(220.0, 224.0)
    )
    parser.add_argument("--iso-carrier", type=float, default=400.0)
    parser.add_argument("--sr", type=int, default=44100)
    parser.add_argument("--out", default=".")
    parser.add_argument("--title-prefix", default="", help="Prefix for track titles.")
    parser.add_argument("--artist", default="TamerOnLine")
    parser.add_argument("--year", default="2025")
    parser.add_argument(
        "--copyright",
        default="© 2025 TamerOnLine. All rights reserved.",
    )
    parser.add_argument("--url", default="https://tameronline.com")
    parser.add_argument("--email", default="info@tameronline.com")
    parser.add_argument("--artwork", default="image/logo.png", help="Path to PNG/JPEG cover.")
    args = parser.parse_args()

    dur = int(args.minutes * 60)
    binaural, iso, sr = make(
        beat_hz=args.freq,
        duration_sec=dur,
        sr=args.sr,
        binaural_carriers=tuple(args.binaural),
        iso_carrier=args.iso_carrier,
        amp=args.amp,
    )

    os.makedirs(args.out, exist_ok=True)

    if args.mode in ("binaural", "both"):
        binaural_path = os.path.join(args.out, f"{args.freq:g}hz_binaural.wav")
        save_wav(binaural_path, binaural, sr)
        set_wav_metadata(
            binaural_path,
            title=f"{args.title_prefix} {args.freq:g} Hz Binaural".strip(),
            artist=args.artist,
            comment="Generated by music4hz",
            year=args.year,
            copyright_=args.copyright,
            url=args.url,
            email=args.email,
            artwork_path=args.artwork,
        )

    if args.mode in ("iso", "both"):
        iso_path = os.path.join(args.out, f"{args.freq:g}hz_iso.wav")
        save_wav(iso_path, iso, sr)
        set_wav_metadata(
            iso_path,
            title=f"{args.title_prefix} {args.freq:g} Hz Isochronic".strip(),
            artist=args.artist,
            comment="Generated by music4hz",
            year=args.year,
            copyright_=args.copyright,
            url=args.url,
            email=args.email,
            artwork_path=args.artwork,
        )

    print("Done.")


if __name__ == "__main__":
    main()
