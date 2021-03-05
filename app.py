from flask import Flask, render_template
from helpers import get_mentions, scrape_news

app = Flask(__name__)

@app.route('/')
def index():
    mw = scrape_news()[0]
    sums = scrape_news()[1]
    return render_template('homepage.html', mentions = get_mentions(), mw_card = zip(mw, sums))

if __name__=='__main__':
    app.run(debug=True)
