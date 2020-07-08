from flask import Flask
from flask import request
from flask import jsonify

import json


app = Flask("Test Server")
stored_value = 0
saved_raw_json = """[{
"author": "Steve McConnell",
"name": "Code Complete",
"published": 1993
},
{
"author": "Steve McConnell",
"name": "Rapid development",
"published": 1996
},
{
"author": "Steve McConnell",
"name": "After the gold rush",
"published": 1999
},
{
"author": "Martin Fowler",
"name": "Refactoring",
"published": 1999
},
{
"author": "Martin Fowler",
"name": "UML distilled",
"published": 1997
}]"""

saved_json = {}

search_results = []


@app.route('/')
def hello():
    return jsonify("Hello!")


@app.route('/save', methods=['POST'])
def save_json():
    try:
        json_content = request.get_json()
        if not request.is_json:
            raise TypeError('Data received is not a json')

        global saved_json
        saved_json = json_content
        return 'Json data stored successfully'

    except (TypeError, KeyError) as e:
        return jsonify('Exception occurred due to invalid input: %s' % str(e)), 400
    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


@app.route('/load', methods=['GET'])
def load_saved_json():
    try:
        global saved_json
        return jsonify(saved_json)
    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


@app.route('/search', methods=['GET', 'POST'])
def search_for_values():
    try:
        exact_text = request.args.get('exact_text')
        portion_text = request.args.get('text')
        order_by = request.args.get('order_by')
        sort_direction = request.args.get('sort_direction')
        global saved_json
        global search_results

        if exact_text:
            # there is exact search term
            search_results = []
            for stored_dict in saved_json:
                for key in stored_dict:
                    if exact_text == key or exact_text == str(stored_dict[key]):
                        search_results.append(stored_dict)
                        break

            if order_by:
                return jsonify(order_list_result(search_results, order_by, sort_direction))

            return jsonify(search_results)

        if portion_text:
            # there is portion text search term
            search_results = []
            for stored_dict in saved_json:
                for key in stored_dict:
                    if portion_text in key or portion_text in str(stored_dict[key]):
                        search_results.append(stored_dict)
                        break

            if order_by:
                return jsonify(order_list_result(search_results, order_by, sort_direction))
            return jsonify(search_results)

    except Exception as e:
        return jsonify('Error occurred due to server error: %s' % str(e)), 500


def order_list_result(list_of_results, order_criteria, sort_direction):
    list_of_results.sort(key=lambda evaluated_dict: evaluated_dict[order_criteria])

    if sort_direction == "desc":
        list_of_results.reverse()
        return list_of_results

    return list_of_results


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
