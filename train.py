import pandas as pd
import pickle
import mlflow
import mlflow.sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocess import clean_text
# Load dataset
df = pd.read_csv(r"C:\SOFTWARE\DEVEOPS\dataset\Resume\resume.csv")

# Input and output
X = df["Resume_str"]
y = df["Category"]
X = X.apply(clean_text)
# Convert text into vectors
tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=20000,
    ngram_range=(1,2),
    sublinear_tf=True
)

X = tfidf.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# MLflow experiment
mlflow.set_experiment("Resume Screening")

with mlflow.start_run():

    # Train model
    model = LinearSVC(C=1.5)

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", accuracy)

    # Log in MLflow
    mlflow.log_param("model", "LinearSVC")
    mlflow.log_param("C", 1.5)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "resume_model")

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Save TF-IDF
pickle.dump(tfidf, open("tfidf.pkl", "wb"))

print("Model saved successfully")