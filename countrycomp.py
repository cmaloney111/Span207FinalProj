import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests
import json
from pytrends.request import TrendReq

def get_interest_over_time(keywords, countries):
    """
    Retrieve Google Trends interest over time for multiple keywords across different countries.
    
    Parameters:
    - keywords (list): List of search terms to analyze
    - countries (list): List of country codes (e.g., 'US', 'GB', 'IN')
    
    Returns:
    - dict: Nested dictionary with interest data.
    """
    # Initialize pytrends
    session = requests.Session()
    session.get('https://trends.google.com')
    cookies_map = session.cookies.get_dict()
    nid_cookie = cookies_map['NID']
    pytrends = TrendReq(hl='en-US', tz=360, retries=5, requests_args={'headers': {'Cookie': f'NID={nid_cookie}'}})

    interest_data = {}

    # Loop through each keyword
    for keyword in keywords:
        interest_data[keyword] = {}

        # Loop through each country
        for country in countries:
            try:
                # Build payload for specific keyword and country
                pytrends.build_payload([keyword], timeframe='today 5-y', geo=country)

                # Get interest over time
                interest_df = pytrends.interest_over_time()

                if not interest_df.empty:
                    # Convert data to dictionary format, converting keys to strings
                    interest_data[keyword][country] = {
                        str(key): value for key, value in interest_df[keyword].to_dict().items()
                    }
                else:
                    interest_data[keyword][country] = {}

            except Exception as e:
                print(f"Error fetching data for {keyword} in {country}: {e}")
                interest_data[keyword][country] = {}

    return interest_data

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

    # Run the analysis
    interest_data = get_interest_over_time(keywords, countries)

    # Save the data to a JSON file
    with open('interest_over_time.json', 'w') as json_file:
        json.dump(interest_data, json_file, indent=4)

    print("Analysis complete. Data saved to 'interest_over_time.json'.")

if __name__ == "__main__":
    main()
