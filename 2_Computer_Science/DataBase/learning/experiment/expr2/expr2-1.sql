DROP TABLE IF EXISTS PR;
-- PERSON(P# Pname, Page, Pgender)
DROP TABLE IF EXISTS PERSON;
DROP TABLE IF EXISTS ROOM;

CREATE TABLE IF NOT EXISTS PERSON (
   Pid INT PRIMARY KEY,
   Pname VARCHAR(50),
   Page INT CHECK (Page > 18),
   Pgender CHAR(1)
);

CREATE TABLE ROOM (
    Rid INT PRIMARY KEY,
    Rname VARCHAR(50),  
    Rarea INT
);

CREATE TABLE PR (
    Pid INT,
    Rid INT,
    Date DATE,
    PRIMARY KEY (Pid, Rid),                     -- set (Pid, Rid) as primary key
    FOREIGN KEY (Pid) REFERENCES PERSON(Pid),   -- set Pid as foreign key to PERSON table
    FOREIGN KEY (Rid) REFERENCES ROOM(Rid)      -- set Rid as foreign key to ROOM table
);

-- SELECT conname, contype FROM pg_constraint WHERE conrelid = 'PERSON'::regclass AND contype = 'c';

ALTER TABLE PERSON ADD COLUMN Ptype CHAR(10);
ALTER TABLE PERSON DROP CONSTRAINT IF EXISTS person_age_check;
ALTER TABLE ROOM ALTER COLUMN Rname TYPE VARCHAR(30);


ALTER TABLE ROOM DROP COLUMN Rarea;


CREATE INDEX idx_room_rid_desc ON ROOM (Rid DESC);
CREATE INDEX idx_person_pid_asc ON PERSON (Pid ASC);


CREATE UNIQUE INDEX idx_person_pname_asc ON PERSON (Pname ASC);


DROP INDEX idx_person_pid_asc;