from flask import Flask, request, Response, jsonify, render_template
import requests
import os
import json
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest, REGISTRY

app = Flask(__name__)

os.environ.setdefault('MODEL_SERVICE_URL', 'http://model-service:5001')
API_HOST = os.environ.get('MODEL_SERVICE_URL')
assert API_HOST, 'Envvar API_HOST is required'

predictions_counter = Counter("predictions_counter", "The number of predictions submitted")
wrong_predictions = Counter("wrong_predictions", "The number of wrong predictions")
correct_predictions = Counter("correct_predictions", "The number of correct predictions")

average_sentiment_score_gauge = Gauge("average_sentiment_score",
                                      "The average sentiment score (scale in between ... to ...)")
length_of_review_histogram = Histogram("length_of_review", "The length of reviews")
positive_to_negative_ratio_summary = Summary("positive_to_negative_ratio",
                                             "The ratio between positive and negative reviews", ["sentiment"])

last_review = None
last_predicted_sentiment = None
positive_count = 0
negative_count = 0


@app.route('/')
def root():
    """
    Root endpoint of the app.
    :return:
    """
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    global last_review, last_predicted_sentiment

    predictions_counter.inc()

    user_input = request.get_data()

    res = requests.post(
        url=request.url.replace(request.host_url, f'{API_HOST}/'),
        headers=request.headers,
        data=user_input,
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [
        (k, v) for k, v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]

    request_data = json.loads(user_input)
    review = request_data["review"]

    response_data = json.loads(res.content)

    # Debugging stuff
    with open('/debugging_output.txt', 'w') as f:
        f.write("sentiment: " + str(response_data["sentiment"]) + "\n")
        f.write("review: " + str(review) + "\n")

    last_predicted_sentiment = response_data["sentiment"]
    last_review = str(review)

    return Response(res.content, res.status_code, headers)


@app.post('/evaluation/wrong')
def handle_wrong():
    wrong_predictions.inc()
    return Response()


@app.post('/evaluation/correct')
def handle_correct():
    ## Only updating other metrics when the prediction is correct
    global positive_count, negative_count

    correct_predictions.inc()

    if last_predicted_sentiment == 'positive':
        positive_count += 1
    elif last_predicted_sentiment == 'negative':
        negative_count += 1

    avg_score = positive_count / (positive_count + negative_count)
    average_sentiment_score_gauge.set(avg_score)

    if last_review is not None:
        length_of_review_histogram.observe(len(last_review))

    # Update summary metric with counts
    positive_to_negative_ratio_summary.labels(sentiment='positive').observe(positive_count)
    positive_to_negative_ratio_summary.labels(sentiment='negative').observe(negative_count)

    print(positive_count, negative_count)

    return Response()


@app.route('/metrics', methods=['GET'])
def metrics():
    response = generate_latest(REGISTRY)
    return Response(response, mimetype="text/plain")


if __name__ == '__main__':
    # host 0.0.0.0 to listen to all ip's
    app.run(host='0.0.0.0', port=5000)
