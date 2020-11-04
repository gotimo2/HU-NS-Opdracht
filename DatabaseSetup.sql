DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE tweets(
tweetid int PRIMARY KEY NOT NULL,
tweettext varchar(150) NOT NULL,
inzender varchar(255) NOT NULL,
tijd timestamp NOT NULL
);

CREATE TABLE behandeldetweets(
tweetid int NOT NULL,
tweetText varchar(150) NOT NULL,
tijd timestamp NOT NULL,
inzender varchar(255) NOT NULL,
commentaar varchar(255),
moderator varchar(255) NOT NULL,
behandelmoment timestamp NOT NULL,
goedgekeurdstatus varchar NOT NULL
);

ALTER TABLE behandeldetweets
ADD CONSTRAINT tweetid FOREIGN KEY (tweetid) REFERENCES tweets(tweetid);