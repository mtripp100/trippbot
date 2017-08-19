create table phrases (
    phrase_id serial primary key,
    latin text not null unique,
    translation text not null,
    notes text default '',
);
