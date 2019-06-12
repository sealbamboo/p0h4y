from flask import Flask, render_template
import json

app = Flask(__name__)

# Read json file
with open('./testData/posts.json', 'r') as f:
    postjson = json.load(f)

@app.route("/")
def hello():
    return render_template('index.html',title='Welcome to Index')

@app.route("/about")
def about():
    return render_template('./homeland/about.html', title='About')


@app.route("/dataset")
def dataset():
    return render_template('./webapp/dataset.html',posts=postjson)


if __name__ == '__main__':
    # Run Debug mode without using env
    app.run(host='0.0.0.0', port=80, debug=True)