from flask import Blueprint, render_template, abort

porfolio = Blueprint('porfolio',__name__,
                    template_folder='templates',
                    static_folder='static')

@porfolio.route('/porfolio')
def home():
    return render_template('./porfolio/index.html')

@porfolio.route('/about')
def about():
    return render_template('./porfolio/about.html')

@porfolio.route('/contact')
def contact():
    return render_template('./porfolio/contact.html')

@porfolio.route('/projects')
def project():
    return render_template('./porfolio/projects.html')