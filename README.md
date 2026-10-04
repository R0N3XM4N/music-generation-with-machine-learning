# Music Generation with ML - Complete Version

Full implementation with 10 classical MIDI files.

## Quick Start

```bash
cd complete
pip install -r requirements.txt
python src/run_all.py
```

## Folder Structure

```
complete/
├── data/
│   ├── raw/          # 10 classical MIDI files
│   └── processed/    # Processed sequences
├── models/           # Saved trained models
├── generated/        # Output MIDI files
├── results/          # Metrics CSV
├── figures/          # Accuracy/Loss charts
├── src/
│   ├── preprocess.py
│   ├── model_naive_bayes.py
│   ├── model_nn.py
│   ├── model_lstm.py
│   ├── model_encdec.py
│   ├── train_all.py
│   ├── generate.py
│   └── run_all.py    # Run everything
├── report/
│   └── report.md
├── requirements.txt
└── README.md
```

## Models
1. Naive Bayes
2. Neural Network (MLP)
3. LSTM
4. Encoder-Decoder RNN

## Outputs
- `generated/*.mid` - 4 generated music files
- `results/model_metrics.csv` - Accuracy/loss data
- `figures/*.png` - Comparison charts
