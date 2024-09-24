-- Active: 1726307624654@@127.0.0.1@5432@school


select 
    sid, count(cid) as num_courses
from 
    CHOICES
group by
    sid
having
    count(cid) >= 3;