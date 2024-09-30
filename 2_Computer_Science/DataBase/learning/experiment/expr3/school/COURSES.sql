-- Active: 1726307624654@@127.0.0.1@5432@school
drop TABLE IF EXISTS COURSES;

CREATE TABLE COURSES(
	cid char(5) NOT NULL PRIMARY KEY,
	cname varchar(30) NOT NULL,
	hour int NULL);

INSERT INTO COURSES VALUES ('10001','database',        96);
INSERT INTO COURSES VALUES ('10002','operating system',        88);
INSERT INTO COURSES VALUES ('10003','computer graphics',        48);
INSERT INTO COURSES VALUES ('10004','java',        48);
INSERT INTO COURSES VALUES ('10005','c++',        60);
INSERT INTO COURSES VALUES ('10006','design pattern',        48);
INSERT INTO COURSES VALUES ('10007','uml',        30);
INSERT INTO COURSES VALUES ('10008','data structure',        60);
INSERT INTO COURSES VALUES ('10009','cryptology',        36);
INSERT INTO COURSES VALUES ('10010','software engineering',        50);
INSERT INTO COURSES VALUES ('10011','distributed computing',        36);
INSERT INTO COURSES VALUES ('10012','erp',        40);
INSERT INTO COURSES VALUES ('10013','artifical intelligence',        46);
INSERT INTO COURSES VALUES ('10014','computer network',        60);
INSERT INTO COURSES VALUES ('10015','tcp/ip protocol',        68);
INSERT INTO COURSES VALUES ('10016','data mining',        40);
INSERT INTO COURSES VALUES ('10017','algorithm',        72);
INSERT INTO COURSES VALUES ('10018','unix/linux',        40);
INSERT INTO COURSES VALUES ('10019','jsp',        28);
INSERT INTO COURSES VALUES ('10020','j2ee',        46);
INSERT INTO COURSES VALUES ('10021','j2me',        40);
INSERT INTO COURSES VALUES ('10022','asp',        30);
INSERT INTO COURSES VALUES ('10023','corba',        36);
INSERT INTO COURSES VALUES ('10024','use case',        18);
INSERT INTO COURSES VALUES ('10025','embeded system',        46);
INSERT INTO COURSES VALUES ('10026','struts',        30);
INSERT INTO COURSES VALUES ('10027','cpu',        28);
INSERT INTO COURSES VALUES ('10028','architectonics',        50);
INSERT INTO COURSES VALUES ('10029','compiling principle',        62);
INSERT INTO COURSES VALUES ('10030','information system',        36);
INSERT INTO COURSES VALUES ('10031','internet',        28);
INSERT INTO COURSES VALUES ('10032','virtual system',        38);
INSERT INTO COURSES VALUES ('10033','real-time system',        48);
INSERT INTO COURSES VALUES ('10034','windows',        18);
INSERT INTO COURSES VALUES ('10035','computer virus',        40);
INSERT INTO COURSES VALUES ('10036','website',        36);
INSERT INTO COURSES VALUES ('10037','software testing',        40);
INSERT INTO COURSES VALUES ('10038','c#',        30);
INSERT INTO COURSES VALUES ('10039','fortran',        36);
INSERT INTO COURSES VALUES ('10040','cobol',        36);
INSERT INTO COURSES VALUES ('10041','basic',        24);
INSERT INTO COURSES VALUES ('10042','c',        48);
INSERT INTO COURSES VALUES ('10043','information security',        40);
INSERT INTO COURSES VALUES ('10044','computer storage',        36);
INSERT INTO COURSES VALUES ('10045','software interface',        24);
INSERT INTO COURSES VALUES ('10046','c++/stl programming',        36);
INSERT INTO COURSES VALUES ('10047','computer interface',        48);
INSERT INTO COURSES VALUES ('10048','data warehouse',        36);
INSERT INTO COURSES VALUES ('10049','project management',        40);
INSERT INTO COURSES VALUES ('10050','digital circuit',        36);
