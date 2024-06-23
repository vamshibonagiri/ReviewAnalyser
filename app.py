from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import pos_tag, word_tokenize

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    review_text = data.get('review', '')

    if not review_text:
        return jsonify({'error': 'No review text provided'}), 400

    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(review_text)
    sentiment = 'positive' if sentiment_scores['compound'] >= 0 else 'negative'
    pos_tags = pos_tag(word_tokenize(review_text))

    response = {
        'sentiment': sentiment,
        'scores': sentiment_scores,
        'pos_tags': pos_tags
    }

    return jsonify(response)

@app.route('/fetch_and_analyze', methods=['POST'])
def fetch_and_analyze():
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    reviews = []
    for review in soup.find_all('div', class_='review'):
        review_text = review.get_text(strip=True)
        reviews.append(review_text)

    sia = SentimentIntensityAnalyzer()
    scored_reviews = [(review, sia.polarity_scores(review)['compound']) for review in reviews]
    top_reviews = [review for review, score in sorted(scored_reviews, key=lambda x: x[1], reverse=True)[:3]]

    return jsonify({'reviews': top_reviews})


if __name__ == '__main__':
    nltk.download('vader_lexicon')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    app.run(debug=True)