import os
from flask import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from retrieval_model.model import getTheAnswer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

# Use a service account
cred = credentials.Certificate(
    '/app/mrjake-a9a2f-firebase-adminsdk-ummkl-eb626db542.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route('/', methods=['POST'])
def mainRoute():
    req = request.get_json(silent=True)
    intent = req["queryResult"]["intent"]["displayName"]
    query = req["queryResult"]["queryText"]
    if intent == "qa_system":
        # qa system function
        return make_response(getTheAnswer(query))
    else:
        # generative chatter bot
        return make_response(jsonify(fulfillmentText="I am Mr Moon !"))
