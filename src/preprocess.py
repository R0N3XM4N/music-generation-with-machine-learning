"""MIDI preprocessing pipeline."""
import os, pickle, numpy as np
from music21 import converter, note, chord

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
SEQ_LENGTH = 64

def extract_notes(midi_path):
    midi = converter.parse(midi_path)
    notes = []
    for element in midi.flatten().notesAndRests:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append(".".join(str(n) for n in element.normalOrder))
    return notes

def prepare_sequences(notes, vocab_size):
    pitchnames = sorted(set(notes))
    note_to_int = {n: i for i, n in enumerate(pitchnames)}
    network_input, network_output = [], []
    for i in range(len(notes) - SEQ_LENGTH):
        network_input.append([note_to_int[n] for n in notes[i:i+SEQ_LENGTH]])
        network_output.append(note_to_int[notes[i+SEQ_LENGTH]])
    network_input = np.reshape(network_input, (len(network_input), SEQ_LENGTH, 1))
    network_input = network_input / float(vocab_size)
    return np.array(network_input), np.array(network_output), pitchnames, note_to_int

def main():
    all_notes = []
    midi_files = [f for f in os.listdir(DATA_DIR) if f.endswith((".mid", ".midi"))]
    print(f"Found {len(midi_files)} MIDI files")
    for f in midi_files:
        n = extract_notes(os.path.join(DATA_DIR, f))
        print(f"  {f}: {len(n)} notes")
        all_notes.extend(n)
    vocab_size = len(set(all_notes))
    print(f"Total: {len(all_notes)} notes, vocab={vocab_size}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(os.path.join(PROCESSED_DIR, "notes.pkl"), "wb") as f:
        pickle.dump(all_notes, f)
    X, y, pitchnames, note_to_int = prepare_sequences(all_notes, vocab_size)
    np.save(os.path.join(PROCESSED_DIR, "network_input.npy"), X)
    np.save(os.path.join(PROCESSED_DIR, "network_output.npy"), y)
    with open(os.path.join(PROCESSED_DIR, "pitchnames.pkl"), "wb") as f:
        pickle.dump(pitchnames, f)
    with open(os.path.join(PROCESSED_DIR, "note_to_int.pkl"), "wb") as f:
        pickle.dump(note_to_int, f)
    print(f"Saved {len(X)} sequences")
    return X, y, vocab_size, pitchnames, note_to_int

if __name__ == "__main__":
    main()
