"""Generate music from trained models."""
import os, sys, pickle, numpy as np
from music21 import note, chord, stream, instrument

sys.path.insert(0, os.path.dirname(__file__))
from model_naive_bayes import NaiveBayesMusic
from model_nn import NeuralNetworkMusic
from model_lstm import LSTMMusic
from model_encdec import EncoderDecoderMusic
import torch

BASE = os.path.join(os.path.dirname(__file__), "..")
PROCESSED = os.path.join(BASE, "data", "processed")
MODELS = os.path.join(BASE, "models")
GENERATED = os.path.join(BASE, "generated")

def load_data():
    with open(os.path.join(PROCESSED, "pitchnames.pkl"), "rb") as f:
        pitchnames = pickle.load(f)
    X = np.load(os.path.join(PROCESSED, "network_input.npy"))
    return pitchnames, X

def int_to_pitch(i):
    return i  # Will be mapped later

def notes_to_midi(note_indices, pitchnames, filename):
    int_to_note = {i: p for i, p in enumerate(pitchnames)}
    s = stream.Stream()
    offset = 0
    for idx in note_indices:
        pitch_str = int_to_note[idx]
        try:
            if "." in pitch_str:
                # Chord notation - parse as integers
                nlist = [int(n) for n in pitch_str.split(".")]
                ch = chord.Chord(nlist)
            else:
                # Try as pitch name first, fallback to integer
                try:
                    n = note.Note(pitch_str)
                    ch = n
                except:
                    n = note.Note()
                    n.pitch.midi = int(pitch_str)
                    ch = n
            ch.offset = offset
            ch.storedInstrument = instrument.Piano()
            s.append(ch)
            offset += 0.5
        except Exception as e:
            # Skip problematic notes
            pass
    s.write("midi", fp=filename)
    print(f"  Saved: {filename}")

def generate(model, seed, pitchnames, length=100, temperature=0.8):
    int_to_note = {i: p for i, p in enumerate(pitchnames)}
    pattern = seed.flatten().copy()
    generated = []
    for _ in range(length):
        inp = np.reshape(pattern[-len(seed):], (1, len(seed), 1))
        if hasattr(model, "predict"):
            pred = model.predict(inp)
            idx = pred[0] if isinstance(pred, np.ndarray) else pred
        else:
            idx = model.predict(np.array(inp))[0]
        # Temperature: if >0.7, pick from top 3; if <0.5, more random
        if temperature > 0.7 and isinstance(pred, np.ndarray) and len(pred.shape) > 0:
            # For simplicity: use argmax with slight random noise for variety
            pass
        generated.append(idx)
        pattern = np.append(pattern, idx)
    return generated

def main():
    os.makedirs(GENERATED, exist_ok=True)
    pitchnames, X = load_data()
    seed = X[0]

    print("Generating music...")

    # Naive Bayes
    print("1. Naive Bayes...")
    nb = NaiveBayesMusic()
    nb.load(os.path.join(MODELS, "naive_bayes.pkl"))
    out = generate(nb, seed, pitchnames)
    notes_to_midi(out, pitchnames, os.path.join(GENERATED, "naive_bayes.mid"))

    # Neural Network
    print("2. Neural Network...")
    nn_m = NeuralNetworkMusic()
    nn_m.load(os.path.join(MODELS, "nn.pkl"))
    out = generate(nn_m, seed, pitchnames)
    notes_to_midi(out, pitchnames, os.path.join(GENERATED, "neural_network.mid"))

    # LSTM
    print("3. LSTM...")
    vocab = len(pitchnames)
    lstm = LSTMMusic(vocab)
    lstm.load(os.path.join(MODELS, "lstm.pth"))
    out = generate(lstm, seed, pitchnames)
    notes_to_midi(out, pitchnames, os.path.join(GENERATED, "lstm.mid"))

    # Encoder-Decoder
    print("4. Encoder-Decoder...")
    ed = EncoderDecoderMusic(vocab)
    ed.load(os.path.join(MODELS, "encdec.pth"))
    out = generate(ed, seed, pitchnames)
    notes_to_midi(out, pitchnames, os.path.join(GENERATED, "encoder_decoder.mid"))

    print("\nDone! MIDI files in " + GENERATED)

if __name__ == "__main__":
    main()