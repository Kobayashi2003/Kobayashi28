# 数据库实验9 - 数据库完整性

## 实验目的

学习实体完整性的建立，以及实践违反实体完整性的结果；学习建立外键，以及利用`FOREIGN KEY... REFERENCES`子句以及各种约束保证参照完整性。

## 课内实验

1. 在数据库`school`中建立表`Stu_Union`，进行主键约束，在没有违反实体完整性的前提下插入并更新一条记录。(参考代码如下：)

```sql
CREATE TABLE Stu_Union(
    sno CHAR(5) NOT NULL UNIQUE,
    sname CHAR(8),
    ssex CHAR(1),
    sage INT,
    sdept CHAR(20),
    CONSTRAINT PK_Stu_Union PRIMARY KEY(sno)
);

insert Stu_Union values('10000','王敏','1',23,'CS');

UPDATE Stu_Union SET sno='' WHERE sdept='CS';
UPDATE Stu_Union SET sno='95002' WHERE sname='王敏';

select * from Stu_Union;
```

2. 演示违反实体完整性的插入操作。（可截屏输出结果）

3. 演示违反实体完整性的更新操作。

4. 为演示参照完整性，建立表`Course`，令`cno`为其主键，并在`Stu_Union`中插入数据。为下面的实验步骤做预先准备。（参考代码如下：）

```sql
insert into Stu_Union values('10001','李明','0',24,'EE');

select * from Stu_Union;

create table Course(
    cno char(4)NOT NULL UNIQUE,
    cname varchar(50)NOT NULL,
    cpoints int,
    constraint PK primary key(cno)
);

insert into Course values('0001','ComputerNetworks',2);
insert into Course values('0002','Database',3);
```

5. 建立表`SC`,令`sno`和`cno`分别为参照`Stu_Union`表以及`Course`表的外键，设定为级联删除，并令`(sno,cno)`为主主键，在不违反参照完整性的前提下，插入数据。(参考代码如下：)

```sql
CREATE TABLE SC(
    sno CHAR(5) REFERENCES Stu_Union(sno) on delete cascade,
    Cno CHAR(4) REFERENCES Course(cno) on delete cascade,
    grade INT,
    CONSTRAINT PK_SC PRIMARY KEY(sno,cno)
);

insert into sc values('95002','0001',2);
insert into sc values('95002','0002',2);
insert into sc values('10001','0001',2);
insert into sc values('10001','0002',2);

select * from SC;
```

6. 演示违反参照完整性的插入操作。
7. 在`Stu_Union`中删除数据，演示级联删除。
8. 在`Course`中删除数据，演示级联删除。


## 自我实践

1. 用`alter table`语句将`SC`表中的`on delete cascade`改为`on delete no action`，重新插入`SC`的数据。重复课内实验中7.和8.，观察结果，分析原因。
2. 使用`alter table`语句将`SC`表中的`on delete cascade`改为`on delete set null`，重新插入`SC`的数据。重复课内实验中7.和8.，观察结果，分析原因。

