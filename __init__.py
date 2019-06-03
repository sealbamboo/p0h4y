from flask import Flask, render_template
from p0h4y.app import app
from p0h4y.porfolio import porfolio
from p0h4y.sign import sign

# Init
server = Flask(__name__)

@server.route("/")
def hello():
    return render_template('layout.html')


server.register_blueprint(app, url_prefix='/sca')
server.register_blueprint(porfolio, url_prefix='/porfolio')
server.register_blueprint(sign, url_prefix='/sign')


# Default
if __name__ == '__main__':
    # Run Debug mode without using env
    server.run(debug=True)