# Complete Version - How to Run

## Location
`C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete`

## Dataset
- **19 MIDI files** (Real Bach & Beethoven music + synthesized)
- **20,638 notes** total
- **126 unique pitches** (vocabulary)
- **20,606 training sequences**

## Results Summary

| Model | Accuracy | Loss |
|-------|----------|------|
| Naive Bayes | 15.63% | 84.37% |
| Neural Network | 7.28% | 92.72% |
| LSTM | 8.06% | 91.94% |
| Encoder-Decoder | 8.06% | 91.94% |

## Files Created
✅ `models/` - All 4 trained models (28MB total)
✅ `figures/model_accuracy.png` - Accuracy comparison chart
✅ `figures/model_loss.png` - Loss comparison chart
✅ `results/model_metrics.csv` - Numeric results
✅ `data/processed/` - Preprocessed sequences

## To Run Everything

```bash
cd "C:\Users\trona\Desktop\College\LAB\ML Lab\MiniProj\complete"

# Step 1: Preprocess (already done)
python src/preprocess.py

# Step 2: Train all models (already done - took ~12 minutes)
python src/train_all.py

# Step 3: Generate music (pending)
python src/generate.py
```

## To Run Just One Step

```bash
# Just preprocessing
python src/preprocess.py

# Just training
python src/train_all.py

# Just generation
python src/generate.py
```

## Quick Overview
The complete version uses **real classical music** from Bach and Beethoven, with a much larger vocabulary (126 notes vs 8) and more realistic melodies. The accuracy is lower because the problem is much harder - predicting from 126 possible notes instead of 8.

## Notes
- Training took ~12 minutes on your machine
- The models work better with more training epochs
- Results are saved and ready for your presentation
- Charts are in `figures/` folder
- Report is in `report/report.md`
