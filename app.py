from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import requests

session = requests.Session()
session.get('https://trends.google.com')
cookies_map = session.cookies.get_dict()
nid_cookie = cookies_map['NID']
print(nid_cookie)
print("hi")

app = Flask(__name__)

pytrends = TrendReq(hl='en-US', tz=360, retries=5, backoff_factor=0.2, requests_args={'headers': {'Cookie': f'NID={nid_cookie}'}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/word_usage', methods=['GET'])
def get_word_usage():
    word = request.args.get('word')
    country = request.args.get('country')

    if not word or not country:
        return jsonify({"error": "Both word and country must be provided"}), 400

    # Convert country to its corresponding ISO code (2-letter code)
    country_codes = {
        'argentina': 'AR', 'spain': 'ES', 'mexico': 'MX'
    }

    country_code = country_codes.get(country.lower())
    if not country_code:
        return jsonify({"error": "Country not supported or incorrect country name"}), 400

    # Build the Google Trends request
    pytrends.build_payload([word], cat=0, timeframe='today 12-m', geo=country_code, gprop='')

    # Get the interest over time data for the word
    try:
        data = pytrends.interest_over_time()
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500

    if data.empty:
        return jsonify({"message": f"No data found for {word} in {country}"}), 404

    # Extract the usage data
    usage = data[word].tolist()

    return jsonify({
        "word": word,
        "country": country,
        "usage": usage
    })

if __name__ == '__main__':
    app.run(debug=True)
