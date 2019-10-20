import dill
import numpy as np
import pandas as pd 
from flask import Blueprint, render_template, request

# Database Stuff
from .database import session
from .models import Dataset, Model, Topic

# Model
from .mhelper import predict_topic, h_g_dictionary, preprocess, h_g_predictor, get_url, split_txt_form_url


# App
app_name = 'SCA |'
app = Blueprint('app',__name__,
                template_folder='templates',
                static_folder='static')
 
@app.route('/')
def home():
    return render_template('./application/index.html',
                            title = 'Welcome to SCA')

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
                            title = app_name + ' Dataset',
                            data = enumerate(dataset))

@app.route('/models')
def model():
    models = session.query(Model).all()
    data = []
    for model in models:
        local_technical = model.technical
        data.append({
                        'name':         model.name,
                        'technical':    local_technical.split(),
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
        prob_topic = []
        for index, score in sorted(h_g_predictor[bow_vector], key=lambda tup: -1*tup[1]):
            prob_topic.append({'score': score, 
                                # 'topic':h_g_spredictor.print_topic(index, 5),
                                'topicid': index
                                })
            # print("Score: {}\t Topic: {}".format(score, h_g_predictor.print_topic(index, 5)))

        item = pd.DataFrame([[textContent]], columns=['text'])
        
        # Preview each topic & explore the words occuring and its relative weight
        # Link: https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/#SQLAlchemy-in-Practice
        # --------------------------------------------------------------------------
        dictionary_topic = session.query(Topic).filter(Topic.model == 'gensim').all()
        
        # Get Topic Name accordingly to database map.
        for key, value in enumerate(prob_topic):
            value['score'] = int(round(value['score'],2)*100)
            value['name'] = dictionary_topic[key].get_name()
            value['display'] = str(int(value['score'])) + '%'
        data = prob_topic
    else:
        data = []

    return render_template('./application/prediction.html',
                            title = app_name + ' Predictions',
                            data = data)

@app.route('/extension')
def extension():

    # Import twitter
    from .twitter import get_dataset

    tweets = get_dataset('bbchealth')
    for tweet in tweets:
        tweet['url'] = get_url(tweet['tweetcontent'])
        tweet['tweetcontent'] = split_txt_form_url(tweet['tweetcontent'])

    return render_template('./application/extension.html',
                            title = app_name + ' Extension',
                            data = enumerate(tweets))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./errors/404.html'), #404