"""Quick export of remaining classical piano MIDI files."""
from music21 import corpus
import os

target_dir = r"C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete\data\raw"

# Continue from where we left off - simpler list focused on single-file works
remaining = [
    'bach/bwv847.mxl',
    'bach/bwv848.mxl',
    'bach/bwv849.mxl',
    'bach/bwv850.mxl',
    'bach/bwv851.mxl',
    'beethoven/opus18no3.mxl',
    'beethoven/opus18no4.mxl',
    'beethoven/opus18no5.mxl',
    'beethoven/opus74.mxl',
    'beethoven/opus132.mxl',
    'mozart/k155/movement1.mxl',
    'mozart/k155/movement2.mxl',
    'mozart/k156/movement1.mxl',
    'mozart/k156/movement2.mxl',
    'mozart/k458/movement1.mxl',
    'mozart/k458/movement2.mxl',
    'mozart/k545/movement1_exposition.mxl',
    'mozart/k80/movement1.mxl',
    'mozart/k80/movement2.mxl',
]

exported = 0
errors = 0

for file_path in remaining:
    out_name = file_path.replace('/', '_').replace('\\', '_').replace('.mxl', '.mid')
    out_path = os.path.join(target_dir, out_name)

    # Skip if exists
    if os.path.exists(out_path):
        print(f"SKIP: {out_name} (exists)")
        continue

    try:
        s = corpus.parse(file_path)
        s.write('midi', fp=out_path)
        exported += 1
        print(f"OK: {file_path}")
    except Exception as e:
        errors += 1
        print(f"ERR: {file_path} -> {e}")

print(f"\n=== New exports: {exported}, Errors: {errors} ===")
