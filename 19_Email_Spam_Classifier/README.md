# Email Spam Classifier

A beginner-friendly machine-learning mini project that classifies email/message text as **spam** or **not spam (ham)** using TF-IDF features and Logistic Regression. The interface is built with Streamlit.

## Features

- Paste an email and classify it interactively.
- Shows an estimated spam score.
- Includes a small example dataset to run immediately.
- Upload your own labeled CSV dataset.
- Shows a held-out accuracy metric and evaluation details.
- Includes readable Python code and a Streamlit interface.

> **Important:** This is an educational demo, not a production email-security system. The included dataset is small, so its predictions and evaluation metrics are not reliable enough for real-world security decisions. It does not connect to Gmail/Outlook or send emails.

## Project structure

```text
email-spam-classifier/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── emails.csv
```

## Run on Windows (VS Code / PowerShell)

1. Extract the ZIP file.
2. Open the extracted `email-spam-classifier` folder in VS Code.
3. Open the terminal in that folder.
4. Create a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app using Streamlit (do **not** run `python app.py`):

   ```powershell
   python -m streamlit run app.py
   ```

7. Open the local address shown in the terminal, usually `http://localhost:8501`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Upload your own dataset

Upload a CSV with a text column and a label column. Common column names are supported:

- Text column: `text`, `message`, `email`, `email_text`, or `content`
- Label column: `label`, `category`, `class`, `target`, or `is_spam`

Example:

```csv
text,label
"Congratulations! You won a free prize. Click now.",spam
"Hi, are we still meeting at 3 pm?",ham
```

Labels accepted: `spam`, `ham`, `not spam`, `not_spam`, `junk`, `legitimate`, `1`, and `0`.

For meaningful evaluation, use a large, balanced, representative, correctly labeled dataset. Avoid uploading sensitive or private emails unless you have permission to process them.

## How it works

1. `TfidfVectorizer` transforms email text into weighted word and phrase features.
2. `LogisticRegression` learns patterns associated with spam and legitimate messages.
3. A held-out split is used to estimate performance when the dataset is large enough.
4. The final model is trained on the available dataset for interactive predictions.

## Ideas for improvements

- Use a larger public spam dataset.
- Compare Naive Bayes, Logistic Regression, and Linear SVM.
- Add precision, recall, F1-score, and a confusion-matrix chart.
- Add language detection and more robust text preprocessing.
- Deploy the Streamlit app.

## License

MIT
