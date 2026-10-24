import re
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).parent
DEFAULT_DATASET = BASE_DIR / "data" / "emails.csv"

st.set_page_config(page_title="Email Spam Classifier", page_icon="📧", layout="wide")

@st.cache_data
def load_default_data():
    return pd.read_csv(DEFAULT_DATASET)

def normalize_label(value):
    value = str(value).strip().lower()
    if value in {"spam", "1", "junk", "yes"}:
        return "spam"
    if value in {"ham", "not spam", "not_spam", "0", "legitimate", "no"}:
        return "ham"
    return None

def prepare_dataset(df):
    # Accept common column names so users can upload their own CSV.
    lower_map = {str(c).strip().lower(): c for c in df.columns}
    text_col = next((lower_map[c] for c in ["text", "message", "email", "email_text", "content"] if c in lower_map), None)
    label_col = next((lower_map[c] for c in ["label", "category", "class", "target", "is_spam"] if c in lower_map), None)
    if text_col is None or label_col is None:
        raise ValueError("CSV must contain a text column (for example 'text') and a label column (for example 'label').")
    result = df[[text_col, label_col]].copy()
    result.columns = ["text", "label"]
    result["text"] = result["text"].fillna("").astype(str).str.strip()
    result["label"] = result["label"].map(normalize_label)
    result = result[(result["text"] != "") & result["label"].notna()].drop_duplicates()
    if result["label"].nunique() < 2:
        raise ValueError("The dataset must contain examples of both spam and ham (not spam).")
    return result

@st.cache_resource
def train_model(dataframe_fingerprint, X, y):
    # Cache key includes a fingerprint generated from the dataset content.
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), max_features=20000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    ])
    pipeline.fit(X, y)
    return pipeline

st.title("📧 Email Spam Classifier")
st.write("Classify an email or message as **spam** or **not spam** using a TF-IDF + Logistic Regression machine-learning pipeline.")
st.caption("This is a learning/demo project. It does not connect to your mailbox or send emails.")

with st.sidebar:
    st.header("Dataset")
    uploaded_file = st.file_uploader("Upload a labeled CSV (optional)", type=["csv"])
    st.markdown("**Expected columns**")
    st.code("text,label\nCongratulations! Claim prize,spam\nHi, meeting at 3 pm,ham")
    st.caption("Labels accepted: spam/ham, 1/0, junk/legitimate.")

try:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file else load_default_data()
    data = prepare_dataset(raw_df)
except Exception as exc:
    st.error(f"Could not load dataset: {exc}")
    st.stop()

if len(data) < 10:
    st.warning("This dataset is very small. Use more labeled examples for more reliable predictions.")

# Keep a held-out test set for a useful demo metric. Train the deployed model on all examples afterwards.
counts = data["label"].value_counts()
can_split = len(data) >= 10 and counts.min() >= 2
if can_split:
    X_train, X_test, y_train, y_test = train_test_split(
        data["text"], data["label"], test_size=0.25, random_state=42, stratify=data["label"]
    )
    evaluation_pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), max_features=20000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    ])
    evaluation_pipeline.fit(X_train, y_train)
    y_pred = evaluation_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    final_model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), max_features=20000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    ])
    final_model.fit(data["text"], data["label"])
else:
    accuracy = None
    final_model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), max_features=20000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    ])
    final_model.fit(data["text"], data["label"])

m1, m2, m3 = st.columns(3)
m1.metric("Training examples", f"{len(data):,}")
m2.metric("Spam examples", f"{(data['label'] == 'spam').sum():,}")
m3.metric("Held-out accuracy", f"{accuracy:.1%}" if accuracy is not None else "N/A")

st.divider()
left, right = st.columns([1.3, 1])
with left:
    st.subheader("Check an email")
    email_text = st.text_area(
        "Paste the email or message below",
        height=220,
        placeholder="Example: Congratulations! You have won a prize. Click here to claim..."
    )
    if st.button("Classify email", type="primary", use_container_width=True):
        if not email_text.strip():
            st.warning("Please enter some email text first.")
        else:
            prediction = final_model.predict([email_text])[0]
            probabilities = final_model.predict_proba([email_text])[0]
            classes = list(final_model.classes_)
            spam_probability = float(probabilities[classes.index("spam")])
            if prediction == "spam":
                st.error("🚨 Prediction: SPAM")
            else:
                st.success("✅ Prediction: NOT SPAM (HAM)")
            st.progress(spam_probability, text=f"Estimated spam score: {spam_probability:.1%}")
            st.caption("The score is a model estimate, not a guarantee. Review suspicious messages carefully.")
with right:
    st.subheader("How it works")
    st.markdown("""
    1. **Text preparation** — clean missing values and normalize labels.
    2. **TF-IDF** — converts words and phrases into numerical features.
    3. **Logistic Regression** — learns patterns from labeled examples.
    4. **Prediction** — returns spam/ham plus an estimated spam score.
    """)
    st.info("Never click links or share personal details just because a message appears as 'not spam'.")

st.divider()
with st.expander("View dataset preview"):
    st.dataframe(data.head(30), use_container_width=True)
with st.expander("Model evaluation details"):
    if can_split:
        st.write(f"**Held-out accuracy:** {accuracy:.3f}")
        st.write("Accuracy is only one measure; a larger and more representative dataset is needed for meaningful evaluation.")
        st.text(classification_report(y_test, y_pred, zero_division=0))
        cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
        st.write("Confusion matrix (rows = actual, columns = predicted; order: ham, spam)")
        st.dataframe(pd.DataFrame(cm, index=["Actual ham", "Actual spam"], columns=["Predicted ham", "Predicted spam"]))
    else:
        st.write("Add more labeled examples (at least 10 total, with both labels represented) to show a held-out evaluation.")
