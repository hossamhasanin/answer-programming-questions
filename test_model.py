import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from retrieval_model.feature_exctractor import *
from retrieval_model.l2_retriever import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import pickle as pk


# Use a service account
cred = credentials.Certificate(
    'mrjake-a9a2f-firebase-adminsdk-ummkl-eb626db542.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

questionsCollection = db.collection("questions").order_by(
    u'question', direction=firestore.Query.DESCENDING).stream()

questions = {}
X = []
for doc in questionsCollection:
    ques = doc.to_dict()
    questions[ques["question"]] = ques
    X.append(ques["question"])

print(X)


# X_square_norm = np.linalg.norm(X_vect, axis=1)

# np.save("questions_square_norm", X_square_norm)

# np.save("questions_embeddings", X_vect)

query = "i need a greate courses for bigenners in android programming"


vectorized_norm = np.load("questions_square_norm.npy")

X_vect = np.load("questions_embeddings.npy")

# score = np.sum(query_vect * X_vect, axis=1) / vectorized_norm


module_url = "https://tfhub.dev/google/universal-sentence-encoder/3"
encoder = SentenceEncoder(module_url)

query_vect = encoder.encode([query])

topk_idx, scores = encoder.find_closest_k_questions(
    1, query_vect, X_vect, vectorized_norm)

# topk_idx = np.argsort(score)[::-1][:1]
for i in topk_idx:
    print(scores[i], X[i])
    print(extract_the_answer(questions[X[i]], db))
