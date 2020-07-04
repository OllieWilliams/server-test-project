from flask import Flask
from flask import request

app = Flask("Test Server")


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/addition', methods=['GET', 'POST'])
def add_variables_with_key():
    a = float(request.args.get('a'))
    b = 0

    return str(a + b)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)