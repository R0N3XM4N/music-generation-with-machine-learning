"""Run the complete project: preprocess -> train -> generate."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from preprocess import main as preprocess
from train_all import main as train
from generate import main as generate

BASE = os.path.join(os.path.dirname(__file__), "..")
print("="*50)
print("MUSIC GENERATION WITH ML - COMPLETE PROJECT")
print("="*50)

print("\n[1/3] Preprocessing...")
preprocess()

print("\n[2/3] Training...")
train()

print("\n[3/3] Generating music...")
generate()

print("\n" + "="*50)
print("ALL DONE! Check generated/ folder for MIDI files.")
print("="*50)
