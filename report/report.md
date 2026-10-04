# Music Generation with Machine Learning
## Complete Project Report

---

## 1. Introduction

This project implements four machine learning approaches to generate classical-style piano music. Using MIDI files, we train models to predict the next note in a sequence, enabling automated music composition.

## 2. Problem Statement

Given a sequence of musical notes, predict the next note to generate coherent music. Four models are compared:
- Naive Bayes (probabilistic)
- Neural Network (feedforward)
- LSTM (recurrent)
- Encoder-Decoder (sequence-to-sequence)

## 3. Dataset

- **Type**: Classical piano MIDI files
- **Source**: Synthesized classical melodies in C major
- **Total Notes**: ~300+ per file × 10 files
- **Vocabulary**: 8-10 unique pitches
- **Format**: Sequences of 32 notes → next note prediction
- **Split**: 70% train / 15% validation / 15% test

## 4. Methodology

### 4.1 Preprocessing
1. Parse MIDI files using music21
2. Extract note/chord information
3. Convert to integer tokens
4. Create sliding window sequences
5. Normalize input features

### 4.2 Feature Representation
- Input: 32-note sequences (normalized)
- Output: Single next-note classification
- Representation: Token-based pitch encoding

## 5. Models

### 5.1 Naive Bayes
- Probabilistic classifier
- P(note | context) with Laplace smoothing
- Fast, simple, good baseline

### 5.2 Neural Network
- 256 → 128 → vocab_size neurons
- ReLU activation
- Early stopping for regularization

### 5.3 LSTM
- Embedding(64) → LSTM(128) → Linear(8)
- Adam optimizer, learning rate 0.001
- 50 training epochs

### 5.4 Encoder-Decoder
- Encoder: Embedding → GRU
- Decoder: Embedding → GRU → Linear
- Sequence-to-sequence architecture

## 6. Evaluation

### Metrics
- **Accuracy**: Next-note prediction accuracy
- **Loss**: Cross-entropy loss
- **Comparison**: Bar charts across models

### Output Files
- `results/model_metrics.csv` - Numeric results
- `figures/model_accuracy.png` - Accuracy comparison
- `figures/model_loss.png` - Loss comparison
- `generated/*.mid` - Generated music files

## 7. Results

Trained models show varying performance:
- Naive Bayes and NN: Strong on simple patterns
- LSTM and Encoder-Decoder: Better with more data

See generated plots and CSV for exact numbers.

## 8. Conclusion

All four models successfully generate music. Naive Bayes and NN work well for simple patterns. LSTM and Encoder-Decoder show potential for more complex compositions with larger datasets.

## 9. References

1. music21 toolkit (Cuthbert & Ariza)
2. PyTorch documentation
3. Scikit-learn documentation
4. Hands-On Machine Learning (Géron, 2017)

---
*Generated for ML Mini Project*