"""SqlAlchemy Models for twitoff"""
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

DB = SQLAlchemy()

# migrate = Migrate()
# subclass of the model class
class User(DB.Model):
    """Twitter users that pull and analyze for """
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False)
    #followers_count = db.Column(db.Integer)
    #follows_count = db.Column(db.Integer)
    latest_tweet_id = DB.Column(DB.BigInteger)
    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(500))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)