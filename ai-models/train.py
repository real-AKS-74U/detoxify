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

vectorizer = CountVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)
model = MultinomialNB()
model.fit(X_train_vectors, Y_train)
Y_pred = model.predict(X_test_vectors)
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Score: {accuracy * 100:.2f}%\n")
print(classification_report(Y_test, Y_pred))

test_comments = [
    "Kon Kon dekh raha hai",#spam
    "2025 wale like thoko",#not_spam(but want to mark this a spam)
    "Only legends with unferstand this",#not_spam(but want to mark this as spam)
    "Buy iphone form here: ",#Scam/spam
    "Hot MILFS in your area",#Scam/spam
    "Who is in march 2025?",#not_spam(but want to mark this a spam)
    "You are such a good youtuber",#not_spam
    "subscribe to this channel",#spam
    "Best vlogger",#spam
    "Jai shree Ram",#not_spam
    "Allah hu Akbar",#maynot_spam
    "Jesus Christ!",#spam
    "Amen!",#not_spam
    "I like your content",#spam(but want to mark this is as  spam)
    "Best video ever",#spam (but want to mark it as not_spam)
    "Marvel fans assemble",#not_spam
    "Jeet gye boyss",#not_spam
    "Shreyas Iyer underarted player",#not_spam



]

test_comments_vector = vectorizer.transform(test_comments)
predictions = model.predict_proba(test_comments_vector)
spam_proba = [pred[1] for pred in predictions]
print("Predictions: " ,spam_proba)




print(predictions)

joblib.dump(vectorizer, 'commentvectorizer.pkl')
joblib.dump(model, 'model.pkl')