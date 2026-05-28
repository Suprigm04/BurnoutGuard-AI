import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# ── Generate synthetic training data ────────────────────────
np.random.seed(42)
n_samples = 1000

data = []
for _ in range(n_samples):
    # Low risk profile
    if np.random.random() < 0.33:
        q1, q2, q3, q4, q5 = np.random.randint(1, 3, 5)
        label = "Low Risk"
    # Moderate risk profile
    elif np.random.random() < 0.66:
        q1, q2, q3, q4, q5 = np.random.randint(2, 4, 5)
        label = "Moderate Risk"
    # High risk profile
    else:
        q1, q2, q3, q4, q5 = np.random.randint(3, 6, 5)
        label = "High Risk"

    score = q1 + q2 + q3 + q4 + q5
    data.append([q1, q2, q3, q4, q5, score, label])

df = pd.DataFrame(
    data, columns=["q1", "q2", "q3", "q4", "q5", "score", "label"])

# ── Train model ──────────────────────────────────────────────
X = df[["q1", "q2", "q3", "q4", "q5", "score"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ── Evaluate ─────────────────────────────────────────────────
print("Model Performance:")
print(classification_report(y_test, model.predict(X_test)))

# ── Save model ───────────────────────────────────────────────
with open("burnout_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as burnout_model.pkl")
