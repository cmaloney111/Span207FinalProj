import requests
from bs4 import BeautifulSoup
from collections import Counter
import time

COUNTRY_SOURCES = {
    "Mexico": [
        "https://www.eluniversal.com.mx/",
        "https://www.milenio.com/",
        "https://www.excelsior.com.mx/"
    ],
    "Argentina": [
        "https://www.clarin.com/",
        "https://www.lanacion.com.ar/",
        "https://www.infobae.com/"
    ],
    "Spain": [
        "https://elpais.com/",
        "https://www.abc.es/",
        "https://www.elmundo.es/"
    ]
}

ANGLICISMS = [
        "internet", "software", "hardware", "email", "smartphone", "streaming", "cloud",
        "wifi", "hashtag", "app", "server", "login", "logout", "password", "startup",
        "blog", "ecommerce", "social media", "online", "offline", "cyber", "network", "web",
        "platform", "AI", "algorithm", "analytics", "data", "digital", "link", "malware",
        "phishing", "bot", "cryptocurrency", "blockchain", "Machine Learning", "Data Science",
        "technology", "innovation", "digital transformation", "tech trends", 
        "computer science", "programming", "tech startup", "tech industry"
    ]

def fetch_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract visible text from <p> tags
        paragraphs = soup.find_all('p')
        text_content = ' '.join(p.get_text() for p in paragraphs)
        return text_content.lower()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def find_all_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = {a.get('href') for a in soup.find_all('a', href=True)}
        return {link for link in links if link.startswith("http")}
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return set()

def scrape_site_recursive(url, visited, anglicisms, depth=1, max_depth=2):
    if depth > max_depth or url in visited:
        return Counter()

    print(f"Scraping: {url} at depth {depth}")
    visited.add(url)

    text = fetch_text_from_url(url)
    anglicism_counts, all_counts = count_anglicisms(text, anglicisms)

    links = find_all_links(url)
    for link in links:
        time.sleep(1)  # Avoid overwhelming server
        spec_count, all_count = scrape_site_recursive(link, visited, anglicisms, depth + 1, max_depth)
        anglicism_counts.update(spec_count)
        all_counts.update(all_count)
        

    return anglicism_counts, all_counts

def count_anglicisms(text, anglicisms):
    word_count = Counter(text.split())
    anglicism_count = {word: word_count[word] for word in anglicisms if word in word_count}
    return Counter(anglicism_count), word_count

def analyze_sources(sources, anglicisms, max_depth):
    country_counts = {}
    all_counts = {}

    for country, urls in sources.items():
        total_counts = Counter()
        total_num_words = Counter()
        visited = set()
        print(f"Analyzing sources for {country}...")

        for url in urls:
            spec_count, all_count = scrape_site_recursive(url, visited, anglicisms, max_depth=max_depth)
            total_counts.update(spec_count)
            total_num_words.update(all_count)

        country_counts[country] = sum(total_counts.values())
        all_counts[country] = sum(total_num_words.values())
        print(f"{country}: {total_counts}")

    return country_counts, all_counts

def main():
    max_depth = 2
    print("Starting...")
    results_country, results_all = analyze_sources(COUNTRY_SOURCES, ANGLICISMS, max_depth)

    print("\nResults:")
    for country, count in results_country.items():
        print(f"{country}: {count} technological anglicisms")

    for country, count in results_all.items():
        print(f"{country}: {count} words")

    most_anglicisms = max(results_country, key=results_country.get)
    print(f"\nThe country with the most technological anglicisms is: {most_anglicisms}")

if __name__ == "__main__":
    main()