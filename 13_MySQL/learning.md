# 资料库管理系统 DBMS（DataBase Management System）

- RDBMS（Relational DataBase Management System）

  - SQL（Structured Query Language）
    - MySQL
    - Oracle
    - PostgreSQL
    - SQL Server

- NRDBMS（Non-Relational DataBase Management System）

  - NoSQL (not just SQL)
    - Redis
    - MongoDB


# MySQL

- primary key 主键
- foreign key 外键

**database**

> create a database
```sql
CREATE DATABASE `database_name`;
```

> show databases
```sql
SHOW DATABASES;
```

> use a database
```sql
USE `database_name`;
```

> remove a database
```sql
DROP DATABASE `database_name`;
```

**table**

- *data type*

  - INT 整数
  - DECIMAL(3,2) 3位整数，2位小数
  - VARCHAR(255) 字符串
  - BLOB （Binary Large Object）二进制对象
  - DATE 'YYYY-MM-DD' 日期
  - TIMESTAMP 'YYYY-MM-DD HH:MM:SS' 时间戳


> create a table
```sql
CREATE TABLE `table_name` (
  `id` INT(11),
  `name` VARCHAR(255),
  `age` INT(11),
  PRIMARY KEY (`id`)
);
```

> show a table
```sql
DESCRIBE `table_name`;
```

> remove a table
```sql
DROP TABLE `table_name`;
```

> add attribute
```sql
ALTER TABLE `table_name` ADD `gender` VARCHAR(255) NOT NULL;
```

> remove attribute
```sql
ALTER TABLE `table_name` DROP COLUMN `gender`;
```

> insert data
```sql
INSERT INTO `table_name` (`id`, `name`, `age`) VALUES (1, 'John', 18);
```

> select data
```sql
SELECT * FROM `table_name`;
```

**constraints** 
<!-- 限制，约束 -->

```sql
CREATE TABLE `table_name` (
  `a` INT NOT NULL, -- not null
  `b` VARCHAR(255) UNIQUE, -- unique value
  `c` INT DEFAULT 0, -- default value
  `d` INT(11) PRIMARY KEY, -- primary key
  `e` INT(11) REFERENCES `table_name`(`id`) -- foreign key
  `f` INT(11) AUTO_INCREMENT -- auto increment
)
```


**修改删除资料**

```sql
UPDATE `student`
SET `major` = `Computer Science`
WHERE `major` = `Computer Engineering` AND `age` > 20;
```

> 关系运算符
  
    - `=` 等于
    - `<>` 不等于
    - `>` 大于
    - `<` 小于
    - `>=` 大于等于
    - `<=` 小于等于
    - `BETWEEN` 在两者之间
    - `LIKE` 模糊查询
    - `IN` 在列表中
    - `IS NULL` 为空
    - `IS NOT NULL` 不为空
  
> 逻辑运算符
    
      - `AND` 与
      - `OR` 或
      - `NOT` 非
  



```sql
DELETE FROM `student`
WHERE `major` = `Computer Science`;
```

```sql
DELETE FROM 'student' -- delete all data
```


**取得资料**

```sql
SELECT * FROM `student`;
```

```sql
SELECT `name`, `age` 
FROM `student` 
WHERE `age` > 20 AND `major` IN ('Computer Science', 'Computer Engineering');
ORDER BY `score`, `age` DESC;
LIMIT 10;
```

