"""Train all four models, evaluate, save metrics and plots."""
import os, sys, pickle, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from model_naive_bayes import NaiveBayesMusic
from model_nn import NeuralNetworkMusic
from model_lstm import LSTMMusic
from model_encdec import EncoderDecoderMusic
import torch

BASE = os.path.join(os.path.dirname(__file__), "..")
PROCESSED = os.path.join(BASE, "data", "processed")
MODELS = os.path.join(BASE, "models")
RESULTS = os.path.join(BASE, "results")
FIGURES = os.path.join(BASE, "figures")

def load_data():
    X = np.load(os.path.join(PROCESSED, "network_input.npy"))
    y = np.load(os.path.join(PROCESSED, "network_output.npy"))
    pitchnames = pickle.load(open(os.path.join(PROCESSED, "pitchnames.pkl"), "rb"))
    return X, y, pitchnames

def split(X, y):
    n = len(X)
    t1, t2 = int(n*0.7), int(n*0.85)
    return X[:t1], y[:t1], X[t1:t2], y[t1:t2], X[t2:], y[t2:]

def main():
    for d in [MODELS, RESULTS, FIGURES]: os.makedirs(d, exist_ok=True)
    X, y, pitchnames = load_data()
    vocab = len(pitchnames)
    Xtr, ytr, Xv, yv, Xte, yte = split(X, y)
    print(f"Data: {len(X)} seq, vocab={vocab}")
    print(f"Train={len(Xtr)}, Val={len(Xv)}, Test={len(Xte)}")

    results = {}

    # 1. Naive Bayes
    print("\n--- Naive Bayes ---")
    nb = NaiveBayesMusic()
    nb.train(Xtr, ytr)
    acc = sum(nb.predict(s)==t for s,t in zip(Xte, yte)) / len(yte)
    print(f"Accuracy: {acc:.4f}")
    nb.save(os.path.join(MODELS, "naive_bayes.pkl"))
    results["Naive Bayes"] = {"accuracy": acc, "loss": 1-acc}

    # 2. Neural Network
    print("\n--- Neural Network ---")
    nn_m = NeuralNetworkMusic()
    nn_m.train(Xtr, ytr)
    acc = nn_m.score(Xte, yte)
    print(f"Accuracy: {acc:.4f}")
    nn_m.save(os.path.join(MODELS, "nn.pkl"))
    results["Neural Network"] = {"accuracy": acc, "loss": 1-acc}

    # 3. LSTM
    print("\n--- LSTM ---")
    lstm = LSTMMusic(vocab)
    lstm.train_model(Xtr, ytr, epochs=100)
    preds = lstm.predict(torch.FloatTensor(Xte))
    acc = np.mean(preds == yte)
    print(f"Accuracy: {acc:.4f}")
    lstm.save(os.path.join(MODELS, "lstm.pth"))
    results["LSTM"] = {"accuracy": acc, "loss": 1-acc}

    # 4. Encoder-Decoder
    print("\n--- Encoder-Decoder ---")
    ed = EncoderDecoderMusic(vocab)
    ed.train_model(Xtr, ytr, epochs=100)
    preds = ed.predict(torch.FloatTensor(Xte))
    acc = np.mean(preds == yte)
    print(f"Accuracy: {acc:.4f}")
    ed.save(os.path.join(MODELS, "encdec.pth"))
    results["Encoder-Decoder"] = {"accuracy": acc, "loss": 1-acc}

    # Save CSV
    with open(os.path.join(RESULTS, "model_metrics.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Model", "Accuracy", "Loss"])
        for name, r in results.items():
            w.writerow([name, f"{r['accuracy']:.4f}", f"{r['loss']:.4f}"])
    print(f"\nMetrics saved to {RESULTS}/model_metrics.csv")

    # --- Plots ---
    models = list(results.keys())
    accs = [results[m]["accuracy"] for m in models]
    losses = [results[m]["loss"] for m in models]
    colors = ["#2ecc71", "#3498db", "#e67e22", "#9b59b6"]

    # Accuracy bar chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(models, accs, color=colors)
    ax.set_title("Model Accuracy Comparison", fontsize=14)
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.1)
    for bar, v in zip(bars, accs):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02, f"{v:.2%}", ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "model_accuracy.png"), dpi=150)
    print("Saved figures/model_accuracy.png")

    # Loss bar chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(models, losses, color=colors)
    ax.set_title("Model Loss Comparison", fontsize=14)
    ax.set_ylabel("Loss (1 - Accuracy)")
    for bar, v in zip(bars, losses):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02, f"{v:.2%}", ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "model_loss.png"), dpi=150)
    print("Saved figures/model_loss.png")

    print("\n=== All models trained ===")
    for m, r in results.items():
        print(f"  {m}: {r['accuracy']:.2%}")

if __name__ == "__main__":
    main()
