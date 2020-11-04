import psycopg2
import dotenv
import os
import datetime
from tkinter import * # pylint: disable=unused-wildcard-import #WaaRoM ImPoRt JE nOu alLEs VaN eEn mODul- STILTE, PYLINT.

dotenv.load_dotenv()

now = datetime.datetime.now()

connection = psycopg2.connect(
    host = os.environ.get("HOST"),
    database = os.environ.get("DATABASE"),
    user = os.environ.get("USER"),
    password = os.environ.get("PASSWORD")
)

cur = connection.cursor()




def stuurTweet():
    print('naamentry')
    naam = NaamEntry.get()
    print(naam)
    if not naam:
        naam = 'anoniem'
    tweet = TweetEntry.get()
    if len(tweet) > 140:

            geefTeLangError(len(tweet) - 140)
    else:
        try:
            print('try gedaan')
            cur.execute("SELECT MAX(tweetid) FROM tweets;")
            newID = int(cur.fetchall()[0][0]) + 1
        except:
            newID = 1         
        formattedTime = now.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO tweets(tweetid, tweettext, inzender, tijd) VALUES(%s, %s, %s, %s)",(newID, tweet, naam, formattedTime))
        print('execute gedaan')
        connection.commit()
        print('Commit gedaan')
        bevestigGestuurd()
        
def geefTeLangError(hoeveelTeLang):
    DynamicLabel['text'] = f'Die tweet is te lang, maak hem {hoeveelTeLang} tekens korter.'

def bevestigGestuurd():
    DynamicLabel['text'] = 'Tweet gestuurd!'
    leegVelden()

def leegVelden():
    TweetEntry.delete(0, 'end')
    NaamEntry.delete(0, 'end')

#defineer window
window = Tk()
window.geometry("1200x700")
window.title("NS Feedback-formulier")
window.configure(bg='#f7d417')

#doe dingen op window
TweetEntry = Entry(
    master=window,
    width=20
)
TweetEntry.place(
    x=500,
    y=350
)
stuurTweetLabel = Label(
    master=window,
    text = 'Stuur ons een tweet met feedback!',
    font = ('Courier', 20),
    fg='blue',
    bg='#f7d417'
)
stuurTweetLabel.place(
    x=320,
    y=150
)
heeftUEvenLabel = Label(
    master=window,
    text = 'Heeft U even?',
    font = ('Courier', 30),
    fg='blue',
    bg='#f7d417'
)
heeftUEvenLabel.place(
    x=400,
    y=100
)

naamLabel = Label(
    master=window,
    text='Uw naam (laat dit leeg voor "anoniem"):',
    fg='blue',
    font = ('Courier', 10),
    bg='#f7d417'
)

tweetLabel = Label(
    master=window,
    text='Uw Tweet (Max. 140 tekens):',
    fg='blue',
    font = ('Courier', 10),
    bg='#f7d417'
)

tweetLabel.place(
    x=280,
    y=350
)
naamLabel.place(
    x=180,
    y=250
)
NaamEntry = Entry(
    master=window
)
NaamEntry.place(
    x=500,
    y=250
)
DynamicLabel = Label(
    master=window,
    width=40,
    bg='#f7d417',
    fg='blue',
    font = ('Courier', 10)
)
DynamicLabel.place(
    x=500,
    y=300
)
emptyButton = Button(
    master=window,
    text="Leeg velden",
    font = ('Courier', 10),
    bg='red',
    fg='white',
    command=leegVelden
)

emptyButton.place(
    x = 515,
    y = 400
)
TweetButton = Button(
    master=window,
    text="Stuur tweet",
    font = ('Courier', 10),
    bg='blue',
    fg='white',
    command=stuurTweet
)
TweetButton.place(
    x = 515,
    y = 450
)

#doe window
window.mainloop()