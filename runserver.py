__author__ = 'ynagai'

from flask import Flask
app = Flask(__name__)

from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path>')
def page(path):
    if not path.endswith('.html'):
        return ''
    return render_template(path)


if __name__ == '__main__':
    app.run(debug=True)
