from flask import Blueprint, render_template
 
app = Blueprint('app',__name__,
                template_folder='templates',
                static_folder='static')
 
@app.route('/')
def home():
    return render_template('./application/index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('./erros/404.html'), #404