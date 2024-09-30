-- Active: 1726307624654@@127.0.0.1@5432@school

select
    sid
from 
    CHOICES
where
    cid in (
        select
            cid
        from
            CHOICES
        where 
            sid = '850955252'
    )
    and sid != '850955252';