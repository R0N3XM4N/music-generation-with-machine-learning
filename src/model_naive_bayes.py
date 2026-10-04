"""Naive Bayes model."""
import pickle, os, numpy as np
from collections import defaultdict, Counter

class NaiveBayesMusic:
    def __init__(self):
        self.context_counts = defaultdict(Counter)
        self.global_counts = Counter()
    def train(self, sequences, targets):
        for seq, target in zip(sequences, targets):
            self.context_counts[tuple(seq.flatten())][target] += 1
            self.global_counts[target] += 1
        self.note_probs = {}
        vocab_size = len(self.global_counts)
        for context, counts in self.context_counts.items():
            total = sum(counts.values())
            self.note_probs[context] = {i: (counts[i]+1)/(total+vocab_size) for i in range(vocab_size)}
    def predict(self, sequence):
        context = tuple(sequence.flatten())
        if context in self.note_probs:
            return max(self.note_probs[context], key=self.note_probs[context].get)
        return self.global_counts.most_common(1)[0][0]
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pickle.dump({"note_probs": self.note_probs, "global_counts": dict(self.global_counts)}, open(path, "wb"))
    def load(self, path):
        data = pickle.load(open(path, "rb"))
        self.note_probs = data["note_probs"]
        self.global_counts = Counter(data["global_counts"])
