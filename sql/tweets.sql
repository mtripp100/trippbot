create table tweets(
    tweet_id text primary key,
    phrase_id integer references phrases(phrase_id) on delete cascade,
    posted_at timestamp without time zone default(now() at time zone 'utc')
);
