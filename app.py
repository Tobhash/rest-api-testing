from flask import Flask

app = Flask(__name__)   # __name__ contains relative path to the module

@app.route('/')         # http://www.mysite.com/
def home():
    return {'message': 'Hello, world!'}


if __name__ == '__main__':
    app.run()