import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from feature_exctractor import *
from l2_retriever import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import pickle as pk


# Use a service account
cred = credentials.Certificate(
    'mrjake-a9a2f-firebase-adminsdk-ummkl-eb626db542.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def getTheAnswer(query):
    questionsCollection = db.collection("questions").order_by(
        u'question', direction=firestore.Query.DESCENDING).stream()

    questions = {}
    X = []
    for doc in questionsCollection:
        ques = doc.to_dict()
        questions[ques["question"]] = ques
        X.append(ques["question"])

    vectorized_norm = np.load("questions_square_norm.npy")

    X_vect = np.load("questions_embeddings.npy")
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/3"
    encoder = SentenceEncoder(module_url)
    query_vect = encoder.encode([query])
    topk = 1
    topk_idx, scores = encoder.find_closest_k_questions(
        topk, query_vect, X_vect, vectorized_norm)

    for i in topk_idx:
        finalAnswer = extract_the_answer(questions[X[i]], db)
        print(scores[i], X[i])
        print(finalAnswer)

    return jsonify(fulfillmentText=finalAnswer)
