import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests
import json
from pytrends.request import TrendReq

def get_interest_by_region_to_json(keywords, countries, output_file):
    """
    Retrieve Google Trends regional interest for multiple keywords and save to JSON file.

    Parameters:
    - keywords (list): List of search terms to analyze
    - countries (list): List of country codes (e.g., 'US', 'GB', 'IN')
    - output_file (str): Path to the JSON file where results will be saved
    """
    # Initialize pytrends
    session = requests.Session()
    session.get('https://trends.google.com')
    cookies_map = session.cookies.get_dict()
    nid_cookie = cookies_map['NID']

    pytrends = TrendReq(hl='en-US', tz=360, retries=5, backoff_factor=0.2, requests_args={'headers': {'Cookie': f'NID={nid_cookie}'}})

    # Dictionary to store all results
    trends_data = {}

    # Loop through each keyword
    for keyword in keywords:
        trends_data[keyword] = {}

        # Loop through each country
        for country in countries:
            try:
                # Build payload for specific keyword and country
                pytrends.build_payload([keyword], geo=country)

                # Get interest by region
                region_df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)

                # Convert to dictionary
                trends_data[keyword][country] = region_df[keyword].to_dict()

            except Exception as e:
                print(f"Error fetching data for {keyword} in {country}: {e}")
                trends_data[keyword][country] = {"error": str(e)}

    # Save results to JSON file
    with open(output_file, 'w') as f:
        json.dump(trends_data, f, indent=4)

    print(f"Data saved to {output_file}")

def main():
    keywords = [
        "internet", "software", "hardware", "email", "smartphone", "streaming", "cloud",
        "wifi", "hashtag", "app", "server", "login", "logout", "password", "startup",
        "blog", "ecommerce", "social media", "online", "offline", "cyber", "network", "web",
        "platform", "AI", "algorithm", "analytics", "data", "digital", "link", "malware",
        "phishing", "bot", "cryptocurrency", "blockchain", "Machine Learning", "Data Science",
        "technology", "innovation", "digital transformation", "tech trends", 
        "computer science", "programming", "tech startup", "tech industry"
    ]
    countries = ['MX', 'ES', 'AR']
    output_file = 'regional_interest_data.json'

    # Run the analysis
    get_interest_by_region_to_json(keywords, countries, output_file)

    print("Analysis complete. Data saved to JSON file.")

if __name__ == "__main__":
    main()
