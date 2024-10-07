create table if not exists vn (
    id              char(10) primary key,
    released        char(10),
    length          integer,
    length_minutes  integer,
    title           text,
    titles          jsonb,
    developers      jsonb,
    platforms       jsonb,
    image           jsonb,
    screenshots     jsonb,
    data            jsonb
);
