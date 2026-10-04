"""Batch export MIDI files from music21 corpus."""
from music21 import corpus
import os

# Target path
target_dir = r"C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete\data\raw"
os.makedirs(target_dir, exist_ok=True)

# List of specific file paths (relative) to export
# Selecting classical piano / keyboard works from corpus
export_list = [
    # Bach - Well-Tempered Clavier I (keyboard/piano)
    'bach/bwv846.mxl',
    'bach/bwv847.mxl',
    'bach/bwv848.mxl',
    'bach/bwv849.mxl',
    'bach/bwv850.mxl',
    'bach/bwv851.mxl',
    # Bach chorales (keyboard works)
    'bach/bwv1.6.mxl',
    'bach/bwv10.7.mxl',
    'bach/bwv102.7.mxl',
    # Beethoven - piano sonata movements
    'beethoven/opus18no1/movement1.mxl',
    'beethoven/opus18no1/movement2.mxl',
    'beethoven/opus18no1/movement3.mxl',
    'beethoven/opus18no1/movement4.mxl',
    'beethoven/opus18no3.mxl',
    'beethoven/opus18no4.mxl',
    'beethoven/opus18no5.mxl',
    'beethoven/opus59no1/movement1.mxl',
    'beethoven/opus59no1/movement2.mxl',
    'beethoven/opus59no1/movement3.mxl',
    'beethoven/opus59no1/movement4.mxl',
    'beethoven/opus59no2/movement1.mxl',
    'beethoven/opus59no2/movement2.mxl',
    'beethoven/opus59no2/movement3.mxl',
    'beethoven/opus59no2/movement4.mxl',
    'beethoven/opus59no3/movement1.mxl',
    'beethoven/opus59no3/movement2.mxl',
    'beethoven/opus59no3/movement3.mxl',
    'beethoven/opus59no3/movement4.mxl',
    'beethoven/opus74.mxl',
    'beethoven/opus132.mxl',
    # Mozart - piano sonatas / concertos
    'mozart/k155/movement1.mxl',
    'mozart/k155/movement2.mxl',
    'mozart/k155/movement3.mxl',
    'mozart/k155/movement4.mxl',
    'mozart/k156/movement1.mxl',
    'mozart/k156/movement2.mxl',
    'mozart/k156/movement3.mxl',
    'mozart/k156/movement4.mxl',
    'mozart/k458/movement1.mxl',
    'mozart/k458/movement2.mxl',
    'mozart/k458/movement3.mxl',
    'mozart/k458/movement4.mxl',
    'mozart/k545/movement1_exposition.mxl',
    'mozart/k80/movement1.mxl',
    'mozart/k80/movement2.mxl',
    'mozart/k80/movement3.mxl',
    'mozart/k80/movement4.mxl',
    # Handel - keyboard suites
    'handel/hwv426.mxl' if False else None,
    'handel/hwv427.mxl',
]

# Filter out None
export_list = [f for f in export_list if f is not None]

exported = []
errors = []

for file_path in export_list:
    out_name = file_path.replace('/', '_').replace('\\', '_')
    # Remove .mxl extension and add .mid
    out_name = out_name.replace('.mxl', '.mid')
    out_path = os.path.join(target_dir, out_name)
    try:
        s = corpus.parse(file_path)
        s.write('midi', fp=out_path)
        exported.append(out_path)
        print(f"OK: {file_path} -> {out_name}")
    except Exception as e:
        errors.append((file_path, str(e)))
        print(f"ERR: {file_path} -> {e}")

print(f"\n=== Exported: {len(exported)}, Errors: {len(errors)} ===")
for e in errors:
    print(f"  ERROR {e[0]}: {e[1]}")
