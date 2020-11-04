#imports

import psycopg2
import datetime     # dit hieronder zorgt ervoor dat je geen waarschuwingen krijgt omdat je 100+ ongebruikte modules import
from tkinter import * # pylint: disable=unused-wildcard-import
from tkinter import messagebox
import time
import dotenv
import os


#definities
now = datetime.datetime.now()

connection = psycopg2.connect(
    host = os.environ.get("HOST"),
    database = os.environ.get("DATABASE"),
    user = os.environ.get("USER"),
    password = os.environ.get("PASSWORD")
)

cur = connection.cursor()

window = Tk()

global nieuweTweets
nieuweTweets = list()

global oordeel
oordeel = StringVar()

def haalTweetsOp():
    cur.execute('SELECT * FROM tweets WHERE tweetid NOT IN (SELECT tweetid FROM behandeldetweets)')
    tweets = cur.fetchall()
    return tweets

naam = 'moderator'

def tweetloop(tweets):
    if not tweets:
        messagebox.showerror("error","Geen onbehandelde tweets gevonden!")
    for i in tweets:
        global oordeel
        oordeel.set('none')
        print('oordeel=none')
        MainLabel['text']= f"{i[3]}:\n {i[2]} schrijft:\n \"{i[1]}\"\n ID {i[0]}"
        print('text set')
        print('wachten op oordeel')
        MainLabel.wait_variable(oordeel) 
        print('oordeel gegeven')
        if oordeel.get() == 'ja':
            print(f"\"{i[1]}\" goedgekeurd")
            commentaar = commentaarEntry.get()
            formattedTime = now.strftime('%Y-%m-%d %H:%M:%S') 
            print('time OK')
            cur.execute("INSERT INTO behandeldetweets(tweetid, tweettext, tijd, inzender, commentaar, moderator, behandelmoment, goedgekeurdstatus) \n VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(i[0], i[1], i[3], i[2], commentaar, naam, formattedTime, "goedgekeurd"))
            connection.commit()
            print('commit OK')
        elif oordeel.get() == 'nee':
            print(f"\"{i[1]}\" afgekeurd")
            commentaar = commentaarEntry.get()
            formattedTime = now.strftime('%Y-%m-%d %H:%M:%S')
            cur.execute(f"INSERT INTO behandeldetweets(tweetid, tweettext, tijd, inzender, commentaar, moderator, behandelmoment, goedgekeurdstatus) \n VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(i[0], i[1], i[3], i[2], commentaar, naam, formattedTime, "afgekeurd"))
            connection.commit()
    MainLabel['text'] = "Alle tweets behandeld!\n Druk op \"Haal tweets op\" om meer tweets op te halen."
    
def ververs():
    global nieuweTweets
    nieuweTweets = haalTweetsOp()
    tweetloop(nieuweTweets)


def doeLoop():
    tweetloop(nieuweTweets)

def jaOordeel():
    global oordeel
    oordeel.set('ja')

def neeOordeel():
    global oordeel
    oordeel.set('nee')



#maak window

window.geometry("800x400")
window.title("NS Moderatie")
window.configure(bg='#f7d417')

#zet dingen op window
    #hallo moderator label
MainLabel = Label(
    text="Hallo, moderator. Druk op de \"Haal tweets op\" knop om te beginnen.",
    bg='#f7d417',
    font=('Courier',10, 'bold'),
    fg='blue'
    )
MainLabel.place(
    x=150,
    y=70
)
    #accept knop
refreshButton = Button(
    master=window,
    text='Haal tweets op',
    command=ververs,
    bg='gray',
    width=10
)

geefCommentaarLabel = Label(
    master=window,
    text='geef commentaar:',
    bg='#f7d417',
    fg='blue',
    font=('Courier',10,'bold')
)

geefCommentaarLabel.place(
    x=170,
    y=250
)

commentaarEntry = Entry(
    master=window,
    text='Commentaar'
)

jaButton= Button(
    master=window,
    text='Goedkeuren',
    bg='green',
    command = jaOordeel,
    width=10
)

jaButton.place(
    x=250,
    y=180
)

neeButton= Button(
    master=window,
    text='Afkeuren',
    bg='red',
    command = neeOordeel,
    width=10
)

neeButton.place(
    x=400,
    y=180
)


commentaarEntry.place(
    x=300,
    y=250
)

refreshButton.place(
    x=0,
    y=0
)

#doe de window
window.mainloop()