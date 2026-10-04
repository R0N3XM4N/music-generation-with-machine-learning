"""LSTM model."""
import torch, torch.nn as nn, numpy as np, os, pickle

class LSTMMusic(nn.Module):
    def __init__(self, vocab_size, hidden=128):
        super().__init__()
        self.hidden = hidden
        self.emb = nn.Embedding(vocab_size, 64)
        self.lstm = nn.LSTM(64, hidden, 1, batch_first=True)
        self.fc = nn.Linear(hidden, vocab_size)
    def forward(self, x):
        x = self.emb(x.long())
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])
    def train_model(self, X, y, epochs=50, lr=0.001):
        X = X.squeeze(-1)
        X_t = torch.FloatTensor(X)
        y_t = torch.LongTensor(y)
        opt = torch.optim.Adam(self.parameters(), lr=lr)
        crit = nn.CrossEntropyLoss()
        self.train()
        for e in range(epochs):
            opt.zero_grad()
            loss = crit(self.forward(X_t), y_t)
            loss.backward()
            opt.step()
            if (e+1) % 10 == 0:
                print(f"  Epoch {e+1}/{epochs}, Loss: {loss.item():.4f}")
    def predict(self, X):
        self.eval()
        X = X.squeeze(-1)
        with torch.no_grad():
            return self.forward(torch.FloatTensor(X)).argmax(dim=1).numpy()
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.state_dict(), path)
    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()
