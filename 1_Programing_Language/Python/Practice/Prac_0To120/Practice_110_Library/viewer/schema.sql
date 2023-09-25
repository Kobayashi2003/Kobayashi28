DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `book_info`;
DROP TABLE IF EXISTS `page_info`;


CREATE TABLE `user` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `username` TEXT NOT NULL,
    `password` TEXT NOT NULL
);


CREATE TABLE `book_info` (
    `title` TEXT PRIMARY KEY,
    `page_count` INTEGER NOT NULL,
    `ctime` DATETIME NOT NULL
);


CREATE TABLE `page_info` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `relpath` TEXT NOT NULL,
    `book_title` TEXT NOT NULL,
    FOREIGN KEY(`book_title`) REFERENCES `book_info`(`title`)
)