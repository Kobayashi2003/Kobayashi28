# 数据库系统实验五 -- 数据查询（嵌套查询）

## 实验目的

熟悉SQL语句的数据查询语言，能够使用SQL语句对数据库进行嵌套查询。

## 实验环境

- OS: Windows 11

![OS](./img/OS.png)

- Database: PostgreSQL 16

![Postgres](./img/Postgres.png)

- UI: harlequin-postgres

![UI](./img/UI.png)

## 实验内容

本节实验的主要内容包括：

- 通过实验验证对子查询的两个限制条件。 
- 体会相关子查询和不相关自查询的不同。 
  - 考察4类谓词的用法，包括：    
  - 第1类，IN，NOT IN；    
  - 第2类，带有比较运算符的子查询；    
  - 第3类，SOME，ANY或ALL谓词的子查询；    
  - 第4类，带有EXISTS谓词的子查询。

## 实验步骤

### 课内实验

要求：

以school数据库为例(与前两次实验的数据同)，在该数据库中存在4张表格，分别为：

    STUDENTS(sid,sname,email,grade)

    TEACHERS(tid,tname,email,salary)

    COURSES(cid,cname,hour)

    CHOICES(no,sid,tid,cid,score)

在数据库中，存在这样的关系：学生可以选择课程。一个课程对应一个教师。在表CHOICES中保存学生的选课记录。

    查询与学号850955252的学生同年级的所有学生资料；

    查询所有的有选课的学生的详细信息；

    查询没有学生选的课程的编号；

    查询选修了课程名为C++的学生学号和姓名；

    找出选修课程成绩最差的选课记录。

    找出和课程UML或课程C++的课时一样的课程名称；

    查询所有选修编号10001的课程的学生的姓名；

    查询选修了所有课程的学生姓名。

**ANSWER**

1. 查询与学号850955252的学生同年级的所有学生资料：

```sql
select *
from students 
where grade = (
  select grade 
  from students 
  where sid = '850955252'
);
```

![001](./img/001.png)

2. 查询所有的有选课的学生的详细信息：

```sql
select *
from students 
where sid in (
  select sid
  from choices 
);
```

![002](./img/002.png)

3. 查询没有学生选的课程的编号：

```sql
select cid
from courses 
where cid not in (
  select cid
  from choices 
);
```

![003](./img/003.png)

4. 查询选修了课程名为C++的学生学号和姓名：

```sql
select sid, sname
from students 
where sid in 
(
  select sid
  from choices 
  where cid = 
  (
    select cid
    from courses 
    where cname = 'c++'
  )
);
```

![004](./img/004.png)

5. 找出选修课程成绩最差的选课记录：

```sql
select *
from choices 
where score = (
  select min(score)
  from choices 
);
```

![005](./img/005.png)

6. 找出和课程UML或课程C++的课时一样的课程名称：

```sql
select cname
from courses 
where hour in (
  select hour 
  from courses 
  where cname in ('uml', 'c++')
);
```

![006](./img/006.png)

7. 查询所有选修编号10001的课程的学生的姓名：

```sql
select sname
from students 
where sid in (
  select sid
  from choices 
  where cid = '10001'
);
```

![007](./img/007.png)

8. 查询选修了所有课程的学生姓名：

```sql
-- I am not recommand this way. It is TOO SLOW.
select sname
from students
where not exists (
  select cid
  from courses
  except 
  select cid 
  from choices
  where choices.sid = students.sid
)
```

或者：

```sql
select sname
from students
where sid in 
(
  select sid
  from choices
  group by sid  
  having count(distinct cid) =
  (
    select count(*)
    from courses
  )
)
```

或者:

```sql
select s.sname from students s
join (
  select sid, count(distinct cid) as num_courses 
  from choices 
  group by sid 
) c on s.sid = c.sid
join (
  select count(*) as num_courses
  from courses
) c2 on c.num_courses = c2.num_courses;
```

![008](./img/008.png)


### 自我实践

    查询选修C++课程的成绩比姓名为znkoo的学生高的所有学生的编号和姓名；

    找出和学生883794999或学生850955252的年级一样的学生的姓名；

    查询没有选修Java的学生名称；

    找出课时最少的课程的详细信息；

    查询工资最高的教师的编号和开设的课程号；

    找出选修课程ERP成绩最高的学生编号；

    查询没有学生选修的课程的名称；

    找出讲授课程UML的教师讲授的所有课程名称；

    查询选修了编号200102901的教师开设的所有课程的学生编号；

    查询选修课程Database的学生集合与选修课程UML的学生集合的并集.


**ANSWER**

1. 查询选修C++课程的成绩比姓名为znkoo的学生高的所有学生的编号和姓名：

```sql
select sid, sname
from students
where sid in 
(
  select stu.sid
  from choices choi, students stu, courses cour
  where choi.sid = stu.sid 
    and choi.cid = cour.cid
    and cour.cname = 'c++'
    and choi.score > 
  (
    select score
    from choices choi2, students stu2, courses cour2
    where choi2.sid = stu2.sid
      and choi2.cid = cour2.cid
      and stu2.sname = 'znkoo'
      and cour2.cname = 'c++'
  )
)
```


![009](./img/009.png)


1. 找出和学生883794999或学生850955252的年级一样的学生的姓名：

```sql
select sname
from students
where grade in 
(
  select grade
  from students
  where sid in ('883794999', '850955252')
)
```

![010](./img/010.png)

3. 查询没有选修Java的学生名称：

```sql
select stu.sname
from students stu
where sid not in 
(
  select sid
  from choices 
  where cid = 
  (
    select cid
    from courses
    where cname = 'java'
  )
)
```

![011](./img/011.png)

4. 找出课时最少的课程的详细信息：

```sql
select *
from courses
where hour = (
  select min(hour)
  from courses
)
```

![012](./img/012.png)

5. 查询工资最高的教师的编号和开设的课程号：

```sql
select tid, cid
from choices
where tid in 
(
  select tid
  from teachers
  where salary = 
  (
    select max(salary)
    from teachers
  )
)
group by tid, cid
```
  
![013](./img/013.png)

6. 找出选修课程ERP成绩最高的学生编号

```sql
select sid
from choices choi, courses cour
where choi.cid = cour.cid
  and cour.cname = 'erp'
  and choi.score = 
(
  select max(score)
  from choices choi2, courses cour2
  where choi2.cid = cour2.cid
    and cour2.cname = 'erp'
)
```

![014](./img/014.png)

7. 查询没有学生选修的课程的名称：

```sql
select cname
from courses
where cid not in (
  select cid
  from choices
)
```

![015](./img/015.png)

8. 找出讲授课程UML的教师讲授的所有课程名称：

```sql
select cname
from courses
where cid in 
(
  select cid
  from choices
  where tid in 
  (
    select tid
    from choices
    where cid =
    (
      select cid
      from courses
      where cname = 'uml'
    )
  )
)
```

![016](./img/016.png)

9. 查询选修了编号200102901的教师开设的所有课程的学生编号：

```sql
select sid
from choices
where sid no in (
  select sid
  from choices
  except 
  select sid
  from choices
  where tid = '200102901'
)
```

![017](./img/017.png)

10. 查询选修课程Database的学生集合与选修课程UML的学生集合的并集：

```sql
select sid
from students
where sid in 
(
  select sid
  from choices
  where cid in 
  (
    select cid
    from courses
    where cname = 'database'
  )
)
union
select sid
from students
where sid in 
(
  select sid
  from choices
  where cid in 
  (
    select cid
    from courses
    where cname = 'uml'
  )
)
```

![018](./img/018.png)


## 实验总结

一到了嵌套查询，CHOICES中庞大的数据量便会带来巨大的挑战。如何合理地组织优化查询语句是本次实验的关键点。