## NS-Feedback-Bot

Heb je ooit het verschrikkelijke idee gekregen: "Let us improve brand perception... with twitter!"
...Nee? Wel, als je het idee krijgt is hier een bot die precies dat doet.

## Benodigdheden

 - Tweepy
 - python-dotenv
 - psycopg2
 - tkinter
 - PostgreSQL database
 - OpenWeatherMap API key
 - Twitter Dev account

## Setup

 1. Clone repository
 2. Maak een nieuwe database in PgAdmin
 3. Run DatabaseSetup.sql om tabellen aan te maken in de database
 4. Vul .env in met details over de database, Twitter en OpenWeatherMap API keys
 5. Run reiziger.py om tweets in te sturen, run moderator.py om tweets te modereren, run bot.py om goedgekeurde tweets te publiceren en run bord.py om de tweets te zien
 6. Klaar!

