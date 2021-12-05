import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def create_cursor():
    connection = sqlite3.connect('chinook.db')
    return connection


@app.route('/names')
def get_names():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT DISTINCT (FirstName) FROM customers')
        data = query.fetchall()

    return jsonify(unique_names=str(len(data)))


@app.route('/customers/')
def get_customers():
    with create_cursor() as cursor:

        conditions = []

        try:
            customer_id = int(request.args['id'])  # id
            conditions.append(f'CustomerId = {customer_id}')
        except (ValueError, KeyError):  # id = not int
            pass

        country = request.args.getlist('country')  # country
        if country:
            n = ", ".join(repr(e) for e in country)
            conditions.append(f'Country IN ({n})')

        fax_parameters = {
            'is_null': 'Fax IS NULL',
            'is_not_null': 'Fax IS NOT NULL',
        }
        fax = fax_parameters.get(request.args.get('fax'))  # fax
        if fax:  # if fax is true
            conditions.append(fax)

            # request
        if conditions:  # if conditions is not empty
            where = ' OR '.join(conditions)  # OR
            query = f'SELECT * FROM customers WHERE {where}'
        else:
            query = 'SELECT * FROM customers'

        customers = cursor.execute(query)

        results = customers.fetchall()
    # print(conditions)
    return jsonify(results)


@app.route('/tracks')
def gef_tracks():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT Count(*) FROM tracks')
        data = query.fetchall()

    return jsonify(data)


@app.route('/tracks-sec')
def gef_tracks_sec():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT Name, Milliseconds/1000 FROM tracks')
        data = query.fetchall()

    return jsonify(data)


if __name__ == '__main__':
    app.run()
