import dill
import numpy as np
import pandas as pd 
from flask import Blueprint, render_template, request

# Database Stuff
from .database import session
from .models import Dataset, Model

# Model
from .mhelper import predict_topic
from config import MODEL_2


# App
app_name = 'SCA |'
app = Blueprint('app',__name__,
                template_folder='templates',
                static_folder='static')
 
@app.route('/')
def home():
    return render_template('./application/index.html')

@app.route('/datasets')
def dataset():
    dataset = session.query(Dataset).all()
    sent_data = []
    for record in dataset:
        obj = {'tweetid':       record.tweetid,
                'date':         record.date,
                'tweetcontent': record.tweetcontent,
                'url':          record.url
                }
        sent_data.append(obj)
    return render_template('./application/dataset.html',
                            title= app_name + ' Dataset',
                            data= enumerate(dataset))

@app.route('/models')
def model():
    models = session.query(Model).all()
    data = []
    for model in models:
        data.append({
                        'name':         model.name,
                        'technical':    model.technical,
                        'description':  model.description,
                        'location':     model.location,
                        'image':        model.image
                    })
    return render_template('./application/model.html',
                            title= app_name + ' Models',
                            data=data)

@app.route('/predictions', methods=['POST', 'GET'])
def prediction():
    '''Gets prediction using the HTML form'''
    if request.method == 'POST':

        inputs = request.form
        textContent = inputs['textcontent']

        item = pd.DataFrame([[textContent]], columns=['text'])
        print("POST: ", textContent)
        print("[ITEMS]: ",item)
    else:
        survive = 0
        dead = 0

    return render_template('./application/prediction.html',
                            title= app_name + ' Predictions')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./erros/404.html'), #404