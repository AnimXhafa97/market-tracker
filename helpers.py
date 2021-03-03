import pandas as pd
import requests
import os
import yfinance as yf
import praw
import schedule
import time
from bs4 import BeautifulSoup, SoupStrainer


client_ID = 'Zum_4b_HUOGdlQ'
SECRET_KEY = 'N8aKuYioWG-Ya68Ii5O12rEBSoUsyA'

R_USER = os.environ.get('r_username')
R_PASS = os.environ.get('r_password')

#read stock market tickers as pandas df
df = pd.read_csv('tickers.csv')

reddit = praw.Reddit(
    client_id=client_ID,
    client_secret=SECRET_KEY,
    username=R_USER,
    password=R_PASS,
    user_agent='USERAGENT'
)



err = ['A', 'OR', 'AM', 'IT', 'TY', 'BE', 'NEXT', 'DD', 'SOS', 'CEO', 'R', 'BIG', 'SNOW']

def get_mentions():

    mentions = {}

    for submission in reddit.subreddit('wallstreetbets').hot(limit=10):

        words = submission.title.split()
        for word in words:
            for symbol in df['Symbol']:
                if word[0] == '$':
                    if word[1:] in mentions:
                        mentions[word[1:]] += 1
                if word == symbol:
                    if word in mentions:
                        mentions[word] += 1
                    else:
                        mentions[word] = 1

    for x in err:
        if x in mentions:
            del mentions[x]

    sorted_mentions = sorted(mentions.items(), key=lambda x: x[1], reverse=True)
    return sorted_mentions


#web scraping
def scrape_news():
    links = []

    marketwatch = requests.get('https://www.marketwatch.com/markets?mod=top_nav').text
    seeking_alpha = requests.get('https://seekingalpha.com/').text

    mw_soup = BeautifulSoup(marketwatch, 'lxml')
    sa_soup = BeautifulSoup(seeking_alpha, 'lxml')

    mw_headlines = mw_soup.find_all('a', class_='link')
    sa_headlines = sa_soup.find_all('h3', class_='ba510-qhu28 d45c6-2hlaP _5a9f8-JdZFq _5a9f8-SfA3O _5a9f8-1qXni')

    for item in mw_headlines:
        if item.find_parent('h3', class_='article__headline') is not None:
            links.append(item)


    return links


#get_mentions()

### AUTOMATION SCRIPT ###
# schedule.every().day.at('9:00').do(get_mentions)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
