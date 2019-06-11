import dill
import numpy as np
import pandas as pd 
from flask import Blueprint, render_template, request

# Database Stuff
from .database import session
from .models import Dataset, Model, Topic

# Model
from .mhelper import predict_topic, h_g_dictionary, preprocess, h_g_predictor


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
        print("RECEIVED: ",len(textContent))

        # Data preprocessing step for the unseen document
        # --------------------------------------------------------------------------
        bow_vector = h_g_dictionary.doc2bow(preprocess(textContent))
        prob_topic = {}
        ATLEAST = 0
        for index, score in sorted(h_g_predictor[bow_vector], key=lambda tup: -1*tup[1]):
            if ATLEAST < 3:
                prob_topic.update({score:h_g_predictor.print_topic(index, 5)})
            # print("Score: {}\t Topic: {}".format(score, h_g_predictor.print_topic(index, 5)))
            ATLEAST += 1
        print(prob_topic)

        item = pd.DataFrame([[textContent]], columns=['text'])
        
        # Preview each topic & explore the words occuring and its relative weight
        # Link: https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/#SQLAlchemy-in-Practice
        # --------------------------------------------------------------------------
        dictionary_topic = session.query(Topic).filter(Topic.model == 'gensim').all()
        print(dictionary_topic)
        # for idx, topic in h_g_predictor.print_topics(-1):
        #     dictionary_topic.update({idx+1: topic})
            # print("Topic: {} \nWords: {} \n".format(idx, topic ))
        

    else:
        survive = 0
        dead = 0

    return render_template('./application/prediction.html',
                            title= app_name + ' Predictions')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./errors/404.html'), #404