create table tweets(
    tweet_id text primary key,
    phrase_id uuid not null,
    posted_at timestamp without time zone default(now() at time zone 'utc')
);
