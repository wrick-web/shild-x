import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- CONFIGURATION ---
DATASET_PATH = '../dataset/phishing_data.csv'
MODEL_PATH = '../models/phishing_model.pkl'
VECTORIZER_PATH = '../models/vectorizer.pkl'

def train_model():
    print("🚀 Starting AI Training Process...")

    # 1. Load Dataset
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: Dataset not found at {DATASET_PATH}")
        return

    print("📊 Loading Data...")
    df = pd.read_csv(DATASET_PATH)
    
    # Check if data is valid
    if 'url' not in df.columns or 'label' not in df.columns:
        print("❌ Error: CSV must have 'url' and 'label' columns")
        return

    # 2. Preprocessing (Convert URL text to Numbers)
    # We use TfidfVectorizer to turn "google.com" into [0.1, 0.5, ...]
    print("🔢 Vectorizing URLs...")
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split('/')) # Simple tokenizer by slash
    X = vectorizer.fit_transform(df['url'])
    y = df['label']

    # 3. Split Data (80% for training, 20% for testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Train the Model (Logistic Regression is fast and good for text)
    print("🧠 Training the Brain...")
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 5. Evaluate Accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Model Trained! Accuracy: {accuracy * 100:.2f}%")

    # 6. Save the Model & Vectorizer
    # We need BOTH later. The vectorizer translates, the model decides.
    print("💾 Saving Artifacts...")
    
    # Create models directory if it doesn't exist
    os.makedirs('../models', exist_ok=True)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)

    print(f"🎉 Success! Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()