from tkinter import * #pylint:disable=unused-wildcard-import
import tweepy
import datetime
import requests, json 
import dotenv
import os

window = Tk()
global amsterdamWeather
amsterdamWeather = dict()

def get_amsterdam_weather():
    city_name = 'Amsterdam' #zet stadnaam
    base_url = "http://api.openweathermap.org/data/2.5/weather?" #basis OWM api link
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY") #API key
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric" #link voor API request 
    response = requests.get(complete_url) #maak een request
    x = response.json() #formatteer wat je uit die request krijgt
    y = x["main"]
    return y

def setPublicWeather():
    global amsterdamWeather
    amsterdamWeather = get_amsterdam_weather()
    window.after(30000, setPublicWeather)

setPublicWeather()

tijdDatumNu = datetime.datetime.now().strftime("%H:%M:%S\n%d-%m-%y")
print(tijdDatumNu)
print(amsterdamWeather['humidity'])

weerLabelText = f'Temperatuur: {amsterdamWeather["temp"]}°C.\n Luchtvochtigheid: {amsterdamWeather["humidity"]}%'
#print(weerLabelText)
print(amsterdamWeather)
#52.370216, 4.895168



auth = tweepy.OAuthHandler(os.environ.get("TWITTER_CONSUMER_KEY"), os.environ.get("TWITTER_CONSUMER_SECRET") )
auth.set_access_token(os.environ.get("TWITTER_KEY"), os.environ.get("TWITTER_SECRET"))

api = tweepy.API(auth)

def haalNieuweTweetsOp():
    now = datetime.datetime.now()
    prev=now-datetime.timedelta(days=1)
    now=now.strftime("%Y-%m-%d")
    prev=prev.strftime("%Y-%m-%d")
    tweets = api.user_timeline(
        id=os.environ.get('BOT_USERNAME'),
        since=prev,
        until=now
    )
    LijstVanNieuweTweets = list()
    for tweet in tweets:
        LijstVanNieuweTweets.append(tweet.text)
    return LijstVanNieuweTweets
        
print(haalNieuweTweetsOp())

def updateTweets():
    tweetsOmTeTonen = haalNieuweTweetsOp()
    try:
        tweetLabel1['text'] = tweetsOmTeTonen[0]
    except:
        tweetLabel1['text'] = ""
    try:
        tweetLabel2['text'] = tweetsOmTeTonen[1]
    except:
        tweetLabel2['text'] = ""
    try:
        tweetLabel3['text'] = tweetsOmTeTonen[2]
    except:
        tweetLabel3['text'] = ""
    window.after(30000, updateTweets)

def updateKlok():
    timeLabel['text'] = datetime.datetime.now().strftime("%H:%M:%S\n%d-%m-%y")
    window.after(1000, updateKlok)

def updateWeer():
    weerLabel['text'] = weerLabelText
    window.after(30000, updateWeer)



window.after(100, updateKlok)
window.after(100, updateWeer)
window.after(100, updateTweets)

window.geometry("1200x700")
window.configure(bg='#f7d417')

weerLabel = Label(
    font=('Arial',20),
    fg='blue',
    bg='#f7d417',
    text='weer'
)
weerLabel.place(
    x=100,
    y=450
)

tweetLabel1 = Label(
    font=('Arial',15),
    fg='blue',
    bg='#f7d417',
    text='',
    width=40
)

tweetLabel2 = Label(
    font=('Arial',15),
    fg='blue',
    bg='#f7d417',
    text='',
    width=40,
)

tweetLabel3 = Label(
    font=('Arial',15),
    fg='blue',
    bg='#f7d417',
    text='',
    width=40
)
reizigersZoalsULabel = Label(
    font=('Arial',15),
    fg='blue',
    bg='#f7d417',
    text='Dit zeggen reizigers zoals U over ons op twitter:',
    width=40
)
reizigersZoalsULabel.place(
    x=450,
    y=75
)
tweetLabel1.place(
    x=450,
    y=150
)

tweetLabel2.place(
    x=450,
    y=350,
)

tweetLabel3.place(
    x=450,
    y=550,
)

timeLabel = Label(
    font=('Arial',60),
    fg='blue',
    bg='#f7d417',
    text='klok'
)
timeLabel.place(
    x=100,
    y=100
)



window.mainloop()
