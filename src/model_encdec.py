"""Encoder-Decoder model."""
import torch, torch.nn as nn, numpy as np, os

class Encoder(nn.Module):
    def __init__(self, vocab_size, hidden):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, 64)
        self.gru = nn.GRU(64, hidden, batch_first=True)
    def forward(self, x):
        return self.gru(self.emb(x.long()))[1]

class Decoder(nn.Module):
    def __init__(self, vocab_size, hidden):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, 64)
        self.gru = nn.GRU(64, hidden, batch_first=True)
        self.fc = nn.Linear(hidden, vocab_size)
    def forward(self, x, hidden):
        out, h = self.gru(self.emb(x.long()), hidden)
        return self.fc(out[:, -1, :]), h

class EncoderDecoderMusic(nn.Module):
    def __init__(self, vocab_size, hidden=128):
        super().__init__()
        self.encoder = Encoder(vocab_size, hidden)
        self.decoder = Decoder(vocab_size, hidden)
    def forward(self, src, tgt):
        hidden = self.encoder(src.squeeze(-1).long())
        return self.decoder(tgt.unsqueeze(1), hidden)[0]
    def train_model(self, X, y, epochs=50, lr=0.001):
        X = X.squeeze(-1)
        X_t = torch.FloatTensor(X)
        y_t = torch.LongTensor(y)
        opt = torch.optim.Adam(self.parameters(), lr=lr)
        crit = nn.CrossEntropyLoss()
        self.train()
        for e in range(epochs):
            opt.zero_grad()
            loss = crit(self.forward(X_t, y_t), y_t)
            loss.backward()
            opt.step()
            if (e+1) % 10 == 0:
                print(f"  Epoch {e+1}/{epochs}, Loss: {loss.item():.4f}")
    def predict(self, X):
        self.eval()
        if isinstance(X, np.ndarray):
            X = X.squeeze(-1)
            X = torch.FloatTensor(X)
        elif isinstance(X, torch.Tensor) and len(X.shape) == 3:
            X = X.squeeze(-1)
        with torch.no_grad():
            hidden = self.encoder(X.long())
            dummy = torch.zeros((X.size(0), 1)).long()
            return self.decoder(dummy, hidden)[0].argmax(dim=1).numpy()
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({"enc": self.encoder.state_dict(), "dec": self.decoder.state_dict()}, path)
    def load(self, path):
        d = torch.load(path)
        self.encoder.load_state_dict(d["enc"])
        self.decoder.load_state_dict(d["dec"])
        self.eval()
