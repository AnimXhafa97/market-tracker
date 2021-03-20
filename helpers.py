import pandas as pd
import requests
import os
import praw
from bs4 import BeautifulSoup, SoupStrainer


mentions = {}


#these need to be environment variables
client_ID = 'Zum_4b_HUOGdlQ'
SECRET_KEY = os.environ.get("REDDIT_SECRET")

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


def get_reddit():
    subreddits = {
        'wallstreetbets': [],
        'stocks': [],
        'investing': [],
        'options': [],
        'thecorporation': []
    }
    # for key in subreddits:
    #     #gets ticker mentions
    #     for submission in reddit.subreddit(key).hot(limit=100):
    #         words = submission.title.split()
    #         for word in words:
    #             for symbol in df['Symbol']:
    #                 if word[0] == '$' and word[1:] == symbol:
    #                     if word[1:] in mentions:
    #                         mentions[word[1:]] += 1
    #                     else:
    #                         mentions[word[1:]] = 1
    #                 if word == symbol:
    #                     if word in mentions:
    #                         mentions[word] += 1
    #                     else:
    #                         mentions[word] = 1

    #gets posts
    for key in subreddits:
        for submission in reddit.subreddit(key).hot(limit=10):
            subreddits[key].append([submission.title, submission.created_utc, submission.score, submission.url])

    #removes potential errors from tickers
    for x in err:
        if x in mentions:
            del mentions[x]

    # sorted_mentions = sorted(mentions.items(), key=lambda x: x[1], reverse=True)
    return subreddits



#web scraping
def scrape_mw():
    mw_links = []
    marketwatch = requests.get('https://www.marketwatch.com/markets?mod=top_nav').text

    mw_soup = BeautifulSoup(marketwatch, 'lxml')
    mw_headlines = mw_soup.find_all('a', class_='link')
    mw_summaries = mw_soup.find_all('p', class_='article__summary')

    for item in mw_headlines:
        if item.find_parent('h3', class_='article__headline') is not None:
            mw_links.append(item)

    return mw_links[0:5], mw_summaries[0:5]

def scrape_in():
    pass

def scrape_morningstar():
    links = []
    morningstar = requests.get('https://www.morningstar.com/markets').text

    soup = BeautifulSoup(morningstar, 'lxml')
    headlines = soup.find_all('a', class_= 'mdc-link mds-list-group__link')

    for item in headlines:
        if item.find_parent('li', class_='mdc-list-group__item mds-list-group__item') is not None:
            links.append(item)

    return links[0:5]


# def get_prices():
#     load_dotenv()
#     fmp_api = os.environ.get('API_KEY')
#
#     prices = []
#
#     symbols = get_reddit()[0]
#     for symbol in symbols:
#         prices.append(fmpsdk.company_profile(apikey=fmp_api, symbol = symbol[0]))
#     return prices


# def scrape_pedia():
#
#     investopedia = request.get('https://www.investopedia.com/markets-news-4427704')
#     pedia_soup = BeautifulSoup(investopedia, 'lxml')
### AUTOMATION SCRIPT ###
# schedule.every().day.at('9:00').do(get_mentions)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
