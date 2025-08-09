"""Generate theta tones as binaural or isochronic audio and write WAV files.

This module provides utilities to synthesize binaural and isochronic tones
centered on a theta beat frequency and to save them to 16-bit PCM WAV files.
All public functions include English docstrings and adhere to PEP 8.
"""

import argparse
import os
import wave
from typing import Tuple

import numpy as np


def save_wav(path: str, data: np.ndarray, sr: int = 44100) -> None:
    """Write a mono or stereo float array in ``[-1, 1]`` to a 16-bit WAV file.

    Args:
        path (str): Output file path.
        data (np.ndarray): Audio samples with shape ``(N, C)`` or ``(N,)``.
            Values must be float32/float64 within ``[-1, 1]``.
        sr (int, optional): Sample rate in Hz. Defaults to ``44100``.

    Returns:
        None

    Notes:
        The function clips to ``[-1, 1]``, scales to int16, and writes the data
        with 16-bit sample width. If a 1-D array is provided, it is treated as
        mono.
    """
    if data.ndim == 1:
        data = data[:, None]

    # Clip and convert to int16
    data_i16 = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)

    with wave.open(path, "w") as wf:
        wf.setnchannels(data_i16.shape[1])
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sr)
        wf.writeframes(data_i16.tobytes())


def make(
    theta_hz: float = 4.0,
    duration_sec: int = 600,
    sr: int = 44100,
    binaural_carriers: Tuple[float, float] = (220.0, 224.0),
    iso_carrier: float = 400.0,
    amp: float = 0.3,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """Generate binaural and isochronic tones at a given theta frequency.

    Args:
        theta_hz (float, optional): Desired beat frequency in Hz. Defaults to
            ``4.0``.
        duration_sec (int, optional): Signal duration in seconds. Defaults to
            ``600``.
        sr (int, optional): Sample rate in Hz. Defaults to ``44100``.
        binaural_carriers (Tuple[float, float], optional): Left and right
            carrier frequencies for binaural beats in Hz. Defaults to
            ``(220.0, 224.0)``.
        iso_carrier (float, optional): Carrier frequency for isochronic tone in
            Hz. Defaults to ``400.0``.
        amp (float, optional): Linear amplitude in ``[0, 1]``. Defaults to
            ``0.3``.

    Returns:
        Tuple[np.ndarray, np.ndarray, int]: A tuple ``(binaural, isochronic, sr)``
        where each array has shape ``(N, 2)`` and dtype ``float32``. A 0.5 s
        fade-in/out envelope is applied.

    Notes:
        Computations use ``float32`` to reduce memory. The binaural output is
        stereo with distinct left and right carriers. The isochronic output is
        stereo with identical channels using a soft AM at ``theta_hz``.
    """
    # Time vector as float32 to reduce memory footprint
    n = int(sr * duration_sec)
    t = np.arange(n, dtype=np.float32) / np.float32(sr)

    # Fade-in/out of 0.5 seconds
    fade = int(sr * 0.5)
    env = np.ones_like(t, dtype=np.float32)
    if fade > 0 and fade * 2 < n:
        env[:fade] = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        env[-fade:] = np.linspace(1.0, 0.0, fade, dtype=np.float32)

    # Float32 constants to keep ufuncs on float32
    two_pi = np.float32(2.0 * np.pi)
    l32 = np.float32(binaural_carriers[0])
    r32 = np.float32(binaural_carriers[1])
    theta32 = np.float32(theta_hz)
    iso_c32 = np.float32(iso_carrier)
    amp32 = np.float32(amp)

    # Binaural: two channels with different carriers
    left = env * amp32 * np.sin(two_pi * l32 * t)
    right = env * amp32 * np.sin(two_pi * r32 * t)
    binaural = np.stack([left, right], axis=1)  # (N, 2) float32

    # Isochronic: soft AM (0..1) at theta_hz on carrier iso_carrier (stereo)
    am = env * (np.float32(0.5) * (np.float32(1.0) + np.sin(two_pi * theta32 * t)))
    iso = am * amp32 * np.sin(two_pi * iso_c32 * t)
    isochronic = np.stack([iso, iso], axis=1)

    return binaural, isochronic, sr


def main() -> None:
    """Parse CLI arguments and render requested audio files to disk.

    The command-line interface supports generating binaural beats, isochronic
    tones, or both, with configurable duration, carriers, amplitude, and
    sample rate.
    """
    parser = argparse.ArgumentParser(
        description="Generate theta tones (binaural / isochronic)."
    )
    parser.add_argument(
        "--mode",
        choices=["binaural", "iso", "both"],
        default="both",
        help="Generation mode.",
    )
    parser.add_argument(
        "--minutes",
        type=float,
        default=30.0,
        help="Duration in minutes.",
    )
    parser.add_argument(
        "--theta",
        type=float,
        default=4.0,
        help="Theta beat frequency (Hz).",
    )
    parser.add_argument(
        "--amp",
        type=float,
        default=0.3,
        help="Signal amplitude in [0, 1].",
    )
    parser.add_argument(
        "--binaural",
        type=float,
        nargs=2,
        metavar=("L", "R"),
        default=(220.0, 224.0),
        help=(
            "Left and right carrier frequencies for binaural beats (Hz)."
        ),
    )
    parser.add_argument(
        "--iso-carrier",
        type=float,
        default=400.0,
        help="Isochronic carrier frequency (Hz).",
    )
    parser.add_argument(
        "--sr",
        type=int,
        default=44100,
        help="Sample rate (Hz).",
    )
    parser.add_argument(
        "--out",
        default=".",
        help="Output directory.",
    )
    args = parser.parse_args()

    dur = int(args.minutes * 60)
    binaural, iso, sr = make(
        theta_hz=args.theta,
        duration_sec=dur,
        sr=args.sr,
        binaural_carriers=tuple(args.binaural),
        iso_carrier=args.iso_carrier,
        amp=args.amp,
    )

    os.makedirs(args.out, exist_ok=True)
    if args.mode in ("binaural", "both"):
        save_wav(
            os.path.join(
                args.out, f"theta_{args.theta:g}hz_binaural.wav"
            ),
            binaural,
            sr,
        )
    if args.mode in ("iso", "both"):
        save_wav(
            os.path.join(args.out, f"{args.theta:g}hz_iso.wav"), iso, sr
        )

    print("Done.")


if __name__ == "__main__":
    main()
