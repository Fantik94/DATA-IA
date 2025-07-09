import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# Scraper les citations
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        quotes.append((text, author))
    return quotes

# Analyser le sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Tester le scraper et l'analyse de sentiment
if __name__ == '__main__':
    url = 'http://quotes.toscrape.com'
    quotes = scrape_quotes(url)
    for text, author in quotes[:5]:  # Limité à 5 citations pour l'exemple
        sentiment = analyze_sentiment(text)
        print(f"Citation: {text}")
        print(f"Auteur: {author}")
        print(f"Sentiment: {'Positif' if sentiment > 0 else 'Négatif' if sentiment < 0 else 'Neutre'}")
        print('-'*50)
