"""Retrive Tweets, embeddings, and persist in the database """
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User
# from dotenv import load_dotenv



# load_dotenv()
TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'), 
                                   config('TWITTER_CONSUMER_SECRET_KEY'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
                              
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))
# TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="OOPS")
# TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", default="OOPS")
# TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
# TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

def add_or_update_user(username):
    """Add or update a user and their tweets, else error if not a Twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)  # Fetch twitter user handle
        # Create SQLAlchemy User db instance
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))

        # Add user to database
        DB.session.add(db_user)

        # Fetch tweets as many as recent as possible with no RT's/Replies.
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False,
                     tweet_mode='extended', since_id=db_user.latest_tweet_id)

        # Check if new or recent tweets exists, if does, get their recent most
        # tweet id
        if tweets:
            db_user.latest_tweet_id = tweets[0].id

        # Loop through newly fetched tweets
        for tweet in tweets:
            # Calculate embedding on the full tweet, but truncate for storing
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweet)
            # Add tweets to the database
            DB.session.add(db_tweet)

    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        # If no errors happend than commit the records
        DB.session.commit()

# def twitter_api_clien():
#     auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
#     print(type(auth))
#     auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
#     client = tweepy.API(auth)
#     print(client)
#     return client

# if __name__ == "__main__":

#     client = twitter_api_client()
#     #print(dir(client))

#     #print("----------")
#     #public_tweets = client.home_timeline()
#     #for tweet in public_tweets:
#     #    print(type(tweet), tweet.text)

#     #print("----------------")
#     #elon_tweets = client.user_timeline("elonmusk")
#     #for tweet in elon_tweets:
#     #    print(type(tweet), tweet.text)

#     print("----------------")
#     elon_tweets = client.user_timeline("elonmusk", tweet_mode="extended")
#     for tweet in elon_tweets:
#         print(type(tweet), tweet.full_text)