"""Export classical piano MIDI files from music21 corpus."""
import os
from music21 import converter, instrument

# Target directory
target_dir = r"C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete\data\raw"
os.makedirs(target_dir, exist_ok=True)

# Select piano-friendly works: multi-movement pieces give us more files
# We'll pick pieces likely to be piano/keyboard and grab individual movements
selected_works = [
    # Beethoven Piano Sonatas (each movement is a separate file)
    ('beethoven', 'opus18no1'),
    ('beethoven', 'opus18no3'),
    ('beethoven', 'opus18no5'),
    ('beethoven', 'opus59no1'),
    ('beethoven', 'opus59no2'),
    ('beethoven', 'opus59no3'),
    # Mozart Piano Sonatas / Concertos
    ('mozart', 'k155'),
    ('mozart', 'k156'),
    ('mozart', 'k458'),
    ('mozart', 'k545'),
    ('mozart', 'k80'),
    # Bach keyboard works
    ('bach', 'bwv846'),    # Well-Tempered Clavier I
    ('bach', 'bwv847'),
    ('bach', 'bwv848'),
    ('bach', 'bwv849'),
    ('bach', 'bwv850'),
    ('bach', 'bwv851'),
    # Handel
    ('handel', 'hwv426'),  # Harpsichord Suite
    ('handel', 'hwv427'),
]

exported = []
errors = []

for composer, work_id in selected_works:
    try:
        work_path = f"{composer}/{work_id}"
        print(f"Parsing {work_path} ...")
        s = converter.parse(work_path)

        # Get parts/instruments
        parts = s.parts
        if parts:
            # If multiple parts, export each part separately
            for i, part in enumerate(parts):
                # Try to identify instrument
                try:
                    instr = part.getInstrument()
                    instr_name = instr.instrumentName if instr else f"Part{i}"
                except Exception:
                    instr_name = f"Part{i}"

                # Export this part
                safe_name = f"{composer}_{work_id}_p{i}_{instr_name.replace(' ', '_').replace('/', '_')}"
                out_path = os.path.join(target_dir, safe_name + ".mid")
                part.write('midi', fp=out_path)
                exported.append(out_path)
                print(f"  -> {safe_name}.mid")
        else:
            # Single stream
            safe_name = f"{composer}_{work_id}"
            out_path = os.path.join(target_dir, safe_name + ".mid")
            s.write('midi', fp=out_path)
            exported.append(out_path)
            print(f"  -> {safe_name}.mid")

    except Exception as e:
        errors.append((f"{composer}/{work_id}", str(e)))
        print(f"  ERROR: {e}")

print(f"\n=== Done: {len(exported)} exported, {len(errors)} errors ===")
if errors:
    print("Errors:")
    for comp, err in errors:
        print(f"  {comp}: {err}")
