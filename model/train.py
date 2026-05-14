import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

# ── LOAD DATA ──
print("Loading data...")
fake = pd.read_csv('model/Fake.csv')
real = pd.read_csv('model/True.csv')

# ── ADD LABELS ──
fake['label'] = 0  # 0 = Fake
real['label'] = 1  # 1 = Real

# ── COMBINE ──
df = pd.concat([fake, real], ignore_index=True)
df = df[['text', 'label']].dropna()

print(f"Total articles: {len(df)}")

# ── SPLIT ──
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'],
    test_size=0.2,
    random_state=42
)

# ── VECTORIZE ──
print("Vectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english'
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# ── TRAIN ──
print("Training model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# ── EVALUATE ──
predictions = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {round(accuracy * 100, 2)}%")

# ── SAVE MODEL ──
print("Saving model...")
os.makedirs('model', exist_ok=True)
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Done! Model saved.")