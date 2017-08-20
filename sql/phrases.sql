create table phrases (
    phrase_id uuid primary key,
    latin text not null,
    translation text not null,
    notes text,
    precedence serial
);
