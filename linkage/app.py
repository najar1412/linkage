from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('hello.cfg')
db = SQLAlchemy(app)

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    link = db.Column(db.String)
    init_date = db.Column(db.DateTime)

    def __init__(self, link, title=None):
        self.link = link
        self.title = title
        self.init_date = datetime.utcnow()


db.create_all()


@app.route('/pop')
def pop():
    links = [
        'http://www.google.com',
        'http://www.dailymail.co.uk',
        'http://www.yahoo.com',
        'http://www.flatlands.io'
    ]

    for link in links:
        new_link = Link(link)
        db.session.add(new_link)
    
    db.session.commit()


    return redirect(url_for('index'))


@app.route('/')
def index():
    links = {
        'status': 'success',
        'message': '',
        'links': Link.query.order_by(Link.init_date.desc()).all()
    }


    return render_template('index.html', links=links)


if __name__ == '__main__':
    app.run()