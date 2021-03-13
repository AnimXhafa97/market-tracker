from flask import Flask, render_template
from helpers import get_reddit, scrape_mw, scrape_ip, get_prices

app = Flask(__name__)

@app.route('/')
def index():
    #marketwatch scrape
    mw_headlines = scrape_mw()[0]
    mw_sums = scrape_mw()[1]

    #investorplace scrape
    ip_headlines = scrape_ip()[0]
    ip_sums = scrape_ip()[1]

    return render_template('homepage.html', mw_card = zip(mw_headlines, mw_sums), ip_card = zip(ip_headlines, ip_sums))

@app.route('/reddit')
def reddit():
    return render_template('reddit.html', posts = get_reddit()[1].items(), mentions = get_reddit()[0], prices = get_prices())

if __name__=='__main__':
    app.run(debug=True)
