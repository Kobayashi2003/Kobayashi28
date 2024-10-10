create table if not exists vn (
    id              char(10) primary key,
    date            timestamp default current_timestamp,
    data            jsonb
);
