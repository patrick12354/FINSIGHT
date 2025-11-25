from flask import Flask, render_template
import requests # Library untuk request ke backend

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5000/api" 

def get_backend_options():
    try:
        # Frontend meminta data ke Backend
        response = requests.get(f"{BACKEND_URL}/options")
        return response.json()
    except:
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profit')
def profit():
    options = get_backend_options()
    return render_template('profit_page.html', form_data=options)

@app.route('/quantity')
def quantity():
    options = get_backend_options()
    return render_template('quantity.html', form_data=options)

@app.route('/classification')
def classification():
    options = get_backend_options()
    return render_template('classification_page.html', form_data=options)

@app.route('/overall')
def overall():
    options = get_backend_options()
    return render_template('overall.html', form_data=options)

@app.route('/collaboration')
def collaboration():
    return render_template('collaboration.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)