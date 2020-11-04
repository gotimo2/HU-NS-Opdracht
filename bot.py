import tweepy
import dotenv
import psycopg2
import os
import time

dotenv.load_dotenv()

connection = psycopg2.connect(
    host = os.environ.get("HOST"),
    database = os.environ.get("DATABASE"),
    user = os.environ.get("USER"),
    password = os.environ.get("PASSWORD")
)

auth = tweepy.OAuthHandler(os.environ.get("TWITTER_CONSUMER_KEY"), os.environ.get("TWITTER_CONSUMER_SECRET") )
auth.set_access_token(os.environ.get("TWITTER_KEY"), os.environ.get("TWITTER_SECRET"))

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def getDBTweets():
    cur = connection.cursor()
    cur.execute("SELECT * FROM behandeldetweets WHERE goedgekeurdstatus = 'goedgekeurd'")
    DBtweets = cur.fetchall()
    return DBtweets

def getOwnTweets():
    tweets = api.user_timeline(
        id=os.environ.get("BOT_USERNAME"),
    )
    listOfTweets=list()
    for tweet in tweets:
        listOfTweets.append(tweet.text)
    return listOfTweets
        
def tweetAllNew():
    DBtweets = getDBTweets()
    myTweets = getOwnTweets()
    for i in DBtweets:
        if f'{i[3]}: \"{i[1]}\"' not in myTweets:
            print(f'{i[3]}: \"{i[1]}\" getweet')
            api.update_status(f'{i[3]}: \"{i[1]}\"')

while True:
    tweetAllNew()
    time.sleep(30)
