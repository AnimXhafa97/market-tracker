from flask import Flask, render_template
import helpers
from helpers import get_reddit, scrape_mw, scrape_morningstar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exists
from flask_migrate import Migrate


# sorted_mentions = sorted(helpers.mentions.items(), key=lambda x: x[1], reverse=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketnews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #creates database instance

class Reddit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable = False)
    mentions = db.Column(db.Integer, unique = False, nullable = False, default = 0)

    def __repr__(self):
        return f"Reddit('{self.ticker}', '{self.mentions}')"

@app.route('/')
def index():
    #marketwatch scrape
    mw_headlines = scrape_mw()[0]
    mw_sums = scrape_mw()[1]

    return render_template('homepage.html', mw_card = zip(mw_headlines, mw_sums), ms_card = scrape_morningstar())

@app.route('/reddit')
def reddit():
    return render_template('reddit.html', posts = get_reddit().items())

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run(debug=True)
