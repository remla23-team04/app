from flask import Flask, request, Response, jsonify, render_template
import requests
import os

app = Flask(__name__)

os.environ.setdefault('MODEL_SERVICE_URL', 'http://model-service:5000')
API_HOST = os.environ.get('MODEL_SERVICE_URL'); assert API_HOST, 'Envvar API_HOST is required'

@app.route('/')
def root():
    """
    Root endpoint of the app.
    :return:
    """
    return render_template("index.html")


@app.route('/predict',methods = ['POST'])
def predict():
    res = requests.post(
        url             = request.url.replace(request.host_url, f'{API_HOST}/'),
        headers         = request.headers,
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )
   
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]

    return Response(res.content, res.status_code, headers)


if __name__ == '__main__':
    # host 0.0.0.0 to listen to all ip's
    app.run(host='0.0.0.0')