# pylint: disable=too-few-public-methods
"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

app = Flask(__name__)

def get_results():
    '''create connection to openaq'''
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    if status != 200:
        raise ValueError('Failed to retrieve data from OpenAQ API')

    # Process results into list of tuples
    results = []
    for measurement in body['results']:
        date = measurement['date']['utc']
        value = measurement['value']
        results.append((date, value))

    return results

@app.route('/')
def root():
    '''what displays in the home route'''
    records = Record.query.filter(Record.value >= 18).all()
    results = [(record.datetime, record.value) for record in records]
    return str(results)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

DB = SQLAlchemy(app)

class Record(DB.Model):
    '''create schema for datatable'''
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String)
    value = DB.Column(DB.Float, nullable=False)


    def __repr__(self):
        return f'Record(datetime={self.datetime}, value={self.value})'

@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    results = get_results()
    for result in results:
        date, value = result
        record = Record(datetime=date, value=value)
        DB.session.add(record)

    DB.session.commit()
    return 'Data refreshed!'
