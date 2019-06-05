from flask import Blueprint, render_template

# Database Stuff
from .database import session
from .models import Dataset

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
        obj = {'tweetid': record.tweetid,
                'date': record.date,
                'tweetcontent': record.tweetcontent,
                'url': record.url}
        sent_data.append(obj)
    return render_template('./application/dataset.html',data= enumerate(dataset))

@app.route('/models')
def model():
    return render_template('./application/model.html')

@app.route('/predictions')
def prediction():
    return render_template('./application/prediction.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./erros/404.html'), #404