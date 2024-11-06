from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/<string:name>')
def hello(name: str):
    return f"Hello {name}!"

@app.route('/gbbt/<string:title>')
def get_book_info_by_title(title: str):
    return title


if __name__ == '__main__':
    app.run()
