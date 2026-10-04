"""Download classical piano MIDI files from public sources."""
import requests
import os
import time

target_dir = r"C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete\data\raw"

# Public domain MIDI files from various sources
# Using direct links to classical piano MIDI files from public repositories
midi_urls = [
    # From various public MIDI archives
    ('https://www.kunstderfuge.com/midi/beethoven_moonlight_1.mid', 'beethoven_moonlight_sonata_1.mid'),
    ('https://www.kunstderfuge.com/midi/beethoven_moonlight_2.mid', 'beethoven_moonlight_sonata_2.mid'),
    ('https://www.kunstderfuge.com/midi/beethoven_moonlight_3.mid', 'beethoven_moonlight_sonata_3.mid'),
    ('https://www.kunstderfuge.com/midi/chopin_prelude_op28_no4.mid', 'chopin_prelude_op28_4.mid'),
    ('https://www.kunstderfuge.com/midi/chopin_prelude_op28_no7.mid', 'chopin_prelude_op28_7.mid'),
    ('https://www.kunstderfuge.com/midi/chopin_nocturne_op9_no2.mid', 'chopin_nocturne_op9_2.mid'),
    ('https://www.kunstderfuge.com/midi/mozart_sonata_k331_1.mid', 'mozart_sonata_k331_1.mid'),
    ('https://www.kunstderfuge.com/midi/mozart_sonata_k331_3.mid', 'mozart_sonata_k331_3_rondo.mid'),
    ('https://www.kunstderfuge.com/midi/bach_prelude_wtc1_c.mid', 'bach_wtc1_prelude_c.mid'),
    ('https://www.kunstderfuge.com/midi/bach_fugue_wtc1_c.mid', 'bach_wtc1_fugue_c.mid'),
    ('https://www.kunstderfuge.com/midi/debussy_clair_de_lune.mid', 'debussy_clair_de_lune.mid'),
    ('https://www.kunstderfuge.com/midi/satie_gymnopedia_1.mid', 'satie_gymnopedia_1.mid'),
]

downloaded = 0
errors = 0

for url, filename in midi_urls:
    output_path = os.path.join(target_dir, filename)

    # Skip if exists
    if os.path.exists(output_path):
        print(f"SKIP: {filename} (exists)")
        continue

    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        downloaded += 1
        print(f"  OK: {filename} ({len(response.content)} bytes)")
        time.sleep(0.5)  # Be nice to the server

    except Exception as e:
        errors += 1
        print(f"  ERR: {filename} -> {e}")

print(f"\n=== Downloaded: {downloaded}, Errors: {errors} ===")
