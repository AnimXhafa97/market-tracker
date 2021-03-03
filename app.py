from flask import Flask, render_template
from helpers import get_mentions, scrape_news

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html', mentions = get_mentions(), mw = scrape_news())

if __name__=='__main__':
    app.run(debug=True)
