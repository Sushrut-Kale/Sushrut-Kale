#!/usr/bin/env python3
"""
generate_naruto_audio.py
Synthesizes the iconic Naruto Theme ("The Rising Fighting Spirit")
intro and main riff using multi-track sound synthesis (Shamisen, Flute, Bass, Taiko Drums)
and renders it to MP3 and MP4 visualizer video using ffmpeg.
"""

import os
import wave
import math
import struct
import random
import subprocess

SAMPLE_RATE = 44100

def note_freq(name):
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
             'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
             'A#': 10, 'Bb': 10, 'B': 11}
    letter = name[:-1]
    octave = int(name[-1])
    semitones = notes[letter] + (octave - 4) * 12 - 9  # A4 = 440
    return 440.0 * (2.0 ** (semitones / 12.0))

def generate_theme_audio():
    BPM = 136.0
    beat_dur = 60.0 / BPM
    total_beats = 32  # 8 bars of 4/4 = ~14.1 seconds
    total_samples = int(total_beats * beat_dur * SAMPLE_RATE)

    left_ch = [0.0] * total_samples
    right_ch = [0.0] * total_samples

    # Helper: add tone with harmonics and envelope
    def add_tone(freq, start_beat, dur_beats, amp=0.3, pan=0.0, instrument="shamisen"):
        start_idx = int(start_beat * beat_dur * SAMPLE_RATE)
        dur_samples = int(dur_beats * beat_dur * SAMPLE_RATE)
        end_idx = min(total_samples, start_idx + dur_samples)

        for i in range(start_idx, end_idx):
            t = (i - start_idx) / SAMPLE_RATE
            dur_sec = dur_samples / SAMPLE_RATE

            # Envelope
            if instrument == "shamisen":
                # Fast attack, exponential decay with plectrum snap
                env = math.exp(-t * 6.0) * min(1.0, t * 150.0)
                # Rich odd & even harmonics for Japanese Shamisen
                val = (1.0 * math.sin(2 * math.pi * freq * t) +
                       0.7 * math.sin(2 * math.pi * 2 * freq * t) +
                       0.5 * math.sin(2 * math.pi * 3 * freq * t) +
                       0.3 * math.sin(2 * math.pi * 4 * freq * t) +
                       0.2 * math.sin(2 * math.pi * 5 * freq * t))
                # Slight distortion/crunch
                val = math.tanh(val * 1.6) * 0.7
            elif instrument == "flute":
                # Shakuhachi breathy vibrato
                vibrato = 1.0 + 0.02 * math.sin(2 * math.pi * 5.5 * t)
                env = math.sin(math.pi * min(1.0, t / dur_sec)) ** 0.5
                val = (1.0 * math.sin(2 * math.pi * freq * vibrato * t) +
                       0.3 * math.sin(2 * math.pi * 2 * freq * vibrato * t) +
                       0.1 * math.sin(2 * math.pi * 3 * freq * vibrato * t))
            elif instrument == "bass":
                # Heavy rock bass
                env = math.exp(-t * 3.5) * min(1.0, t * 100.0)
                val = (1.0 * math.sin(2 * math.pi * freq * t) +
                       0.5 * math.sin(2 * math.pi * 2 * freq * t))
                val = math.tanh(val * 1.5)
            else:
                env = math.exp(-t * 4.0)
                val = math.sin(2 * math.pi * freq * t)

            sample = val * env * amp
            left_ch[i] += sample * (1.0 - max(0.0, pan))
            right_ch[i] += sample * (1.0 + min(0.0, pan))

    # Helper: Taiko kick & snare drums
    def add_taiko(beat, is_kick=True):
        start_idx = int(beat * beat_dur * SAMPLE_RATE)
        dur_samples = int(0.35 * SAMPLE_RATE)
        end_idx = min(total_samples, start_idx + dur_samples)

        for i in range(start_idx, end_idx):
            t = (i - start_idx) / SAMPLE_RATE
            if is_kick:
                # Pitch drop from 140Hz to 45Hz
                f = 45.0 + 95.0 * math.exp(-t * 25.0)
                env = math.exp(-t * 9.0)
                val = math.sin(2 * math.pi * f * t) * env * 0.45
            else:
                # Snare crack + noise
                f = 180.0 * math.exp(-t * 30.0)
                noise = random.uniform(-1.0, 1.0)
                env = math.exp(-t * 15.0)
                val = (0.5 * math.sin(2 * math.pi * f * t) + 0.5 * noise) * env * 0.35

            left_ch[i] += val
            right_ch[i] += val

    # MELODY: The iconic "The Rising Fighting Spirit" riff (D Insen scale)
    # Phrase 1: D, D, F, G, G#, G, F, D
    riff_1 = [
        ("D4", 0.0, 0.5), ("D4", 0.5, 0.5), ("F4", 1.0, 0.5), ("G4", 1.5, 0.5),
        ("G#4", 2.0, 0.75), ("G4", 2.75, 0.5), ("F4", 3.25, 0.5), ("D4", 3.75, 0.5),
        # Phrase 2: D, F, G, G#, C5, B4, G
        ("D4", 4.0, 0.5), ("F4", 4.5, 0.5), ("G4", 5.0, 0.5), ("G#4", 5.5, 0.75),
        ("C5", 6.25, 0.75), ("B4", 7.0, 0.5), ("G4", 7.5, 0.5),
        # Phrase 3: D, D, F, G, G#, G, F, D
        ("D4", 8.0, 0.5), ("D4", 8.5, 0.5), ("F4", 9.0, 0.5), ("G4", 9.5, 0.5),
        ("G#4", 10.0, 0.75), ("G4", 10.75, 0.5), ("F4", 11.25, 0.5), ("D4", 11.75, 0.5),
        # Phrase 4: C, D, F, D (Grand Battle Cadence)
        ("C4", 12.0, 0.5), ("D4", 12.5, 0.75), ("F4", 13.25, 0.75), ("D4", 14.0, 1.5)
    ]

    # Repeat riff twice (bars 0-16 and 16-32)
    for rep in [0.0, 16.0]:
        for note, start_b, dur_b in riff_1:
            # Main Shamisen Lead
            add_tone(note_freq(note), rep + start_b, dur_b, amp=0.35, pan=-0.2, instrument="shamisen")
            # Layered Octave Up Shamisen
            oct_note = note[0] + ('#' if '#' in note else '') + str(int(note[-1]) + 1)
            add_tone(note_freq(oct_note), rep + start_b, dur_b, amp=0.22, pan=0.2, instrument="shamisen")
            # Shakuhachi Flute doubling the epic high notes
            if rep >= 16.0:
                add_tone(note_freq(oct_note), rep + start_b, dur_b, amp=0.18, pan=0.0, instrument="flute")

    # BASSLINE (driving rock bass)
    for bar in range(8):
        b = bar * 4.0
        add_tone(note_freq("D2"), b + 0.0, 0.75, amp=0.35, instrument="bass")
        add_tone(note_freq("D2"), b + 1.0, 0.75, amp=0.35, instrument="bass")
        add_tone(note_freq("F2"), b + 2.0, 0.5, amp=0.35, instrument="bass")
        add_tone(note_freq("G2"), b + 2.5, 0.5, amp=0.35, instrument="bass")
        add_tone(note_freq("G#2"), b + 3.0, 0.5, amp=0.35, instrument="bass")
        add_tone(note_freq("G2"), b + 3.5, 0.5, amp=0.35, instrument="bass")

    # DRUMS (Taiko Rock Beat)
    for beat in range(total_beats):
        if beat % 2 == 0:
            add_taiko(beat, is_kick=True)
        else:
            add_taiko(beat, is_kick=False)
        # Extra 16th-note drum rolls on bar transitions
        if beat in [7, 15, 23, 31]:
            add_taiko(beat + 0.5, is_kick=False)
            add_taiko(beat + 0.75, is_kick=True)

    # Normalize audio to prevent clipping
    max_val = 0.001
    for i in range(total_samples):
        max_val = max(max_val, abs(left_ch[i]), abs(right_ch[i]))

    scale = 0.88 / max_val
    for i in range(total_samples):
        left_ch[i] *= scale
        right_ch[i] *= scale

    # Write WAV file
    os.makedirs("assets/audio", exist_ok=True)
    wav_path = "assets/audio/naruto-theme.wav"
    mp3_path = "assets/audio/naruto-theme.mp3"

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for i in range(total_samples):
            # Clamp to 16-bit signed int
            l_int = max(-32767, min(32767, int(left_ch[i] * 32767)))
            r_int = max(-32767, min(32767, int(right_ch[i] * 32767)))
            frames.extend(struct.pack("<hh", l_int, r_int))
        wf.writeframes(frames)

    print(f"[+] Generated WAV: {wav_path} ({len(frames)} bytes, {total_beats * beat_dur:.1f}s)")

    # Encode to MP3 with ffmpeg
    cmd_mp3 = ["ffmpeg", "-y", "-i", wav_path, "-b:a", "192k", mp3_path]
    subprocess.run(cmd_mp3, check=True)
    print(f"[+] Generated MP3: {mp3_path}")

    # Remove temporary WAV
    if os.path.exists(wav_path):
        os.remove(wav_path)

if __name__ == "__main__":
    generate_theme_audio()
