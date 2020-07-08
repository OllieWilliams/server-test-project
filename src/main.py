from flask import Flask
from flask import request
from flask import jsonify


app = Flask("Test Server")
stored_value = 0


@app.route('/')
def hello():
    return jsonify("Hello!")


@app.route('/addition', methods=['GET', 'POST'])
def add_values_with_key():
    try:
        a = request.args.get('a')
        b = request.args.get('b')

        if a is None:
            raise KeyError('Could not find a')
        if b is None:
            raise KeyError('Could not find b')

        if not a.isnumeric():
            raise TypeError('Value of a is not a number')
        if not b.isnumeric():
            raise TypeError('Value of b is not a number')

        return jsonify(float(a) + float(b))

    except (TypeError, KeyError) as e:
        return jsonify('Exception occurred due to invalid input: %s' % str(e)), 400
    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


@app.route('/memory', methods=['PUT'])
def store_value():
    try:
        value_to_store = request.form.get('value')

        if value_to_store is None:
            raise KeyError('Could not find key: value')
        if not value_to_store.isnumeric():
            raise TypeError('value is not a number')

        global stored_value
        stored_value = value_to_store
        return jsonify('Value %s has been stored successfully.' % str(stored_value))

    except (KeyError, TypeError) as e:
        return jsonify('Exception occurred with error: %s' % str(e)), 400
    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


@app.route('/memory', methods=['GET'])
def retrieve_stored_value():
    try:
        global stored_value
        return jsonify(stored_value)

    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
