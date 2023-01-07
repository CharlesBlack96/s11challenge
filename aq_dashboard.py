"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import requests
import openaq

app = Flask(__name__)

api = openaq.OpenAQ() 

@app.route('/')
def get_results():
    """Base view."""
    response = requests.get('https://api.openaq.org/v1/measurements?city=Los Angeles&parameter=pm25')
    return response.text




