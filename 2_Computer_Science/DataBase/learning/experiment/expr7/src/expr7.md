# 实验七 视图

## 实验目的

熟悉SQL语言支持的有关视图的操作，能够熟练使用SQL语句来创建需要的视图，对视图进行查询和取消视图。

## 实验内容

1. 定义常见的视图形式，包括：

- 行列子集视图。
- WITH CHECK OPTION的视图。
- 基于多个基表的视图。
- 基于视图的视图。
- 带表达式的视图。
- 分组视图。

2. 通过实验考察WITH CHECK OPTION这一语句在视图定义后产生的影响，包括对修改操作、删除操作、插入操作的影响。
3. 讨论视图的数据更新情况，对子行列视图进行数据更新。
4. 使用DROP语句删除一个视图，由该视图导出的其他视图定义仍在数据字典中，但已不能使用，必须显式删除。同样的原因，删除基表时，由该基表导出的所有视图定义都必须显式删除。

## 课内实验

**要求：**

以school数据库为例(与之前实验的数据同)，在该数据库中存在4张表格，分别为：

STUDENTS(sid,sname,email,grade)

TEACHERS(tid,tname,email,salary)

COURSES(cid,cname,hour)

CHOICES(no,sid,tid,cid,score)

**CS视图的创建**

```sql
CREATE VIEW CS
AS SELECT NO, SID, CID, SCORE
FROM CHOICES
WHERE SCORE >= 60;
```

**SCT视图的创建**

```sql
CREATE VIEW SCT
(SNAME, CNAME, TNAME)
AS SELECT STUDENTS.SNAME, COURSES.CNAME, TEACHERS.TNAME
FROM CHOICES, STUDENTS, COURSES, TEACHERS
WHERE CHOICE.TID = TEACHERS.TID AND CHOICES.CID = COURSES.CID
  AND CHOICES.SID = STUDENTS.SID;
```

1. 创建一个行列子集视图，给出选课成绩合格的学生的编号，所选课程号和该课程成绩

```sql
CREATE VIEW PASSING_CHOICE AS
SELECT SID, CID, SCORE
FROM CHIOCES
WHERE SCORE >= 60;

SELECT * FROM PASSING_CHOICE;
```

2. 创建基于多个基表的视图，这个视图由学生姓名和其所选修的课程名及讲授该课程的教师姓名构成

```sql
CREATE VIEW STUDENT_COURSE_TEACHER AS
SELECT STUDENTS.SNAME, COURSES.CNAME, TEACHERS.TNAME
FROM STUDENTS S
JOIN CHOICES CH ON S.SID = CH.SID
JOIN COURSES C ON CH.CID = C.CID
JOIN TEACHERS T ON CH.TID = T.TID;

SELECT * FROM STUDENT_COURSE_TEACHER;
```

3. 创建带表达式的视图，由学生姓名、所选课程名和所有课程成绩都比原来多5分这几个属性组成

```sql
CREATE VIEW SCORE_PLUS_FIVE AS
SELECT S.SNAME, C.CNAME, CH.SCORE + 5 AS SCORE_PLUS_FIVE
FROM STUDENTS S
JOIN CHOICES CH ON S.SID = CH.SID
JOIN COURSES C ON CH.CID = C.CID;

SELECT * FROM SCORE_PLUS_FIVE;
```

4. 创建分组视图，将学生的学号及其平均成绩定义为一个视图

```sql
CREATE VIEW STUDENT_AVG_SCORE AS
SELECT SID, AVG(SCORE) AS AVG_SCORE
FROM STUDENTS S
JOIN CHOICES CH ON S.SID = CH.SID
JOIN COURSES C ON CH.CID = C.CID;

SELECT * FROM STUDENT_AVG_SCORE;
```

5. 创建一个基于视图的视图，基于(1)中建立的视图，定义一个包括学生编号，学生所选课程数目和平均成绩的视图

```sql
CREATE VIEW STUDENT_COURSE_STATS AS
SELECT SID,
       COUNT(*) AS COURSE_COUNT,
       AVG(SCORE) AS AVG_SCORE
FROM PASSING_CHOICE
GROUP BY SID;

SELECT * FROM STUDENT_COURSE_STATS;
```

6. 查询所有选修课程Software Engineering的学生姓名

```sql
CREATE VIEW SNAME_SE AS
SELECT DISTINCT S.SNAME
FROM STUDENTS S
JOIN CHOICES CH ON S.SID = CH.SID
JOIN COURSES C ON CH.CID = C.CID
WHERE C.CNAME = "Software Engineering";

SELECT * FROM SNAME_SE;
```

7. 插入元组(600000000,823069829,10010,59)到视图CS中。若是在视图的定义中存在`WITH CHECK OPTION`子句对插入操作有什么影响?

```sql
INSERT INTO CS (NO, SID, CID, SOCRE)
VALUES (600000000, 823069829, 10010, 59);
```

如果视图CS的定义中包含`WITH CHECK OPTION`子句，这个插入将会失败，因为插入的成绩59不满足视图CS定义中的条件`(SCORE >= 60)`。

8. 将视图CS (包含定义WITH CHECK OPTION)中，所有课程编号为10010的课程的成绩都减去5分。这个操作数据库是否会正确执行，为什么?如果加上5分(原来95分以上的不变)呢?

- 减5分操作：

```sql
UPDATE CS
SET SCORE = SCORE - 5
WHERE CID = 10010;
```

这个操作不会正确执行，因为`WITH CHECK OPTION`会则指任何不满足视图条件的更新。减5分可能会导致某些记录的分数低于60，违反了视图的定义条件。

- 加5分（原来95分以上的不变）操作：

```sql
UPDATE CS
SET SCORE = CASE
    WHEN SCORE <= 95 THEN SCORE + 5
    ELSE SCORE
END
WHERE CID = 10010;
```



1. 在视图CS (包含定义WITH CHECK OPTION)删除编号为804529880学生的记录，会产生什么结果?
2.  取消视图SCT和视图CS


## 自我实践

1. 定义选课信息和课程名称的视图VIEWC
2. 定义学生姓名与选课信息的视图VIEWS
3. 定义年级低于1998的学生的视图S1(SID,SNAME,GRADE)
4. 查询学生为“uxjof”的学生的选课信息
5. 查询选修课程“UML”的学生的编号和成绩
6. 向视图S1插入记录(“60000001,Lily,2001”)
7. 定义包括更新和插入约束的视图S1，尝试向视图插入记录(“60000001,Lily,1997")，删除所有年级为1999的学生记录，讨论更新和插入约束带来的影响
8. 在视图VIEWS中将姓名为“uxjof”的学生的选课成绩都加上5分
9. 取消以上建立的所有视图
