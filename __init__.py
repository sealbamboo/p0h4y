from flask import Flask, render_template
from .components import app, porfolio, sign

# Init server
server = Flask(__name__)

@server.route("/")
def hello():
    return render_template('layout.html')


server.register_blueprint(app, url_prefix='/sca')
server.register_blueprint(porfolio, url_prefix='/')
server.register_blueprint(sign, url_prefix='/sign')


# Run Server
if __name__ == '__main__':
    # Run Debug mode without using env
    server.run(debug=True, port=8081, host='0.0.0.0')