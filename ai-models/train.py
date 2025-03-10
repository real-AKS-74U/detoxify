import pandas as pd
import joblib
from sklearn.feature_extraction.text import *
from sklearn.naive_bayes import *
from sklearn.model_selection import *
from sklearn.metrics import *
from huggingface_hub import *

splits = {'train': 'data/train-00000-of-00001-daf190ce720b3dbb.parquet', 'test': 'data/test-00000-of-00001-fa9b3e8ade89a333.parquet'}
df = pd.read_parquet("hf://datasets/Deysi/spam-detection-dataset/" + splits["train"])
data = df
X = data['text']
Y = data['label']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=45)

vectorizer = TfidfVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)
model = MultinomialNB()
model.fit(X_train_vectors, Y_train)
Y_pred = model.predict(X_test_vectors)
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Score: {accuracy * 100:.2f}%\n")
print(classification_report(Y_test, Y_pred))

test_comments = [
    "Kon Kon dekh raha hai",
    "2025 wale like thoko",
    "Only legends with unferstand this",
    "Buy iphone form here: ",
    "Hot MILFS in your area",
    "Who is in march 2025?",
    "You are such a good youtuber",
    "Best vlogger",
    "Jai shree Ram",
    "Allah hu Akbar",
]

test_comments_vector = vectorizer.transform(test_comments)
predictions = model.predict_proba(test_comments_vector)
spam_proba = [pred[1] for pred in predictions]
print("Predictions: ",spam_proba)


#results = {comment: 'spam' if pred == 1 else 'not_spam' for comment, pred in zip(test_comments, predictions)}

#for comment, label in results.items():
#    print(f"Comment: '{comment}' is marked as: {label}")

#print(predictions)

joblib.dump(vectorizer, 'commentvectorizer.pkl')
joblib.dump(model, 'model.pkl')
