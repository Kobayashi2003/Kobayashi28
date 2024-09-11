-- drop the table if it exists
DROP TABLE IF EXISTS `road_position_edge`;
DROP TABLE IF EXISTS `road_position_point`;
DROP TABLE IF EXISTS `road`;
DROP TABLE IF EXISTS `building_position`;
DROP TABLE IF EXISTS `building`;
DROP TABLE IF EXISTS `building_type`;
DROP TABLE IF EXISTS `campus`;

-- CREATE DATABASE `school_map_db`;

-- create the campus table, the postal code should be 6 digits
CREATE TABLE `campus` (
    `campus_id`   INTEGER PRIMARY KEY AUTO_INCREMENT,
    `campus_name` TEXT NOT NULL,
    `campus_addr` TEXT NOT NULL,
    `campus_area` TEXT NOT NULL,
    `campus_info` TEXT,
    `postal_code` INTEGER NOT NULL,
    CHECK (LENGTH(postal_code) = 6)
);
-- test insert campus
-- INSERT INTO `campus` (`campus_name`, `campus_addr`, `campus_area`, `campus_info`, `postal_code`) VALUES ('NCTU', 'No. 1001, University Road, East District, Hsinchu City, Taiwan 300', 'East District', 'National Chiao Tung University', 300000);


-- create the building_type table
CREATE TABLE `building_type` (
    `building_type_id`  INTEGER PRIMARY KEY AUTO_INCREMENT,
    `building_type`     TEXT NOT NULL
);

-- create the building table
CREATE TABLE `building` (
    `building_id`       INTEGER PRIMARY KEY AUTO_INCREMENT,
    `building_name`     TEXT,
    `building_number`   INTEGER,
    `building_type_id`  INTEGER NOT NULL,
    `building_info`     TEXT,
    FOREIGN KEY(`building_type_id`) REFERENCES `building_type`(`building_type_id`),
    CHECK (building_name IS NOT NULL OR building_number IS NOT NULL)
);


-- building position
CREATE TABLE `building_position` (
    `campus_id`     INTEGER NOT NULL,
    `building_id`   INTEGER NOT NULL,
    PRIMARY KEY (`campus_id`, `building_id`),
    `x`             INTEGER NOT NULL,
    `y`             INTEGER NOT NULL,
    `width`         INTEGER NOT NULL,
    `height`        INTEGER NOT NULL,
    `map_width`     INTEGER NOT NULL,
    `map_height`    INTEGER NOT NULL,
    FOREIGN KEY(`campus_id`) REFERENCES `campus`(`campus_id`),
    FOREIGN KEY(`building_id`) REFERENCES `building`(`building_id`),
    CHECK (x >= 0 AND y >= 0 AND width > 0 AND height > 0 AND map_width > 0 AND map_height > 0)
);


-- create the road table
CREATE TABLE `road` (
    `road_id`       INTEGER PRIMARY KEY AUTO_INCREMENT,
    `road_name`     TEXT,
    `road_number`   INTEGER,
    `road_info`     TEXT,
    CHECK (road_name IS NOT NULL OR road_number IS NOT NULL)
);

-- road point 
CREATE TABLE `road_position_point` (
    `point_id`      INTEGER PRIMARY KEY AUTO_INCREMENT,
    `campus_id`     INTEGER NOT NULL,
    `road_id`       INTEGER NOT NULL,
    `point_x`       INTEGER NOT NULL,
    `point_y`       INTEGER NOT NULL,
    `point_radius`  INTEGER NOT NULL,
    `point_info`    TEXT,
    FOREIGN KEY(`campus_id`) REFERENCES `campus`(`campus_id`),
    FOREIGN KEY(`road_id`) REFERENCES `road`(`road_id`),
    CHECK (point_radius >= 0 AND point_x >= 0 AND point_y >= 0)
);

-- road edge
CREATE TABLE `road_position_edge` (
    `edge_id`       INTEGER PRIMARY KEY AUTO_INCREMENT,
    `campus_id`     INTEGER NOT NULL,  
    `road_id`       INTEGER NOT NULL,
    `point_id_1`    INTEGER NOT NULL,
    `point_id_2`    INTEGER NOT NULL,
    `edge_info`     TEXT,
    FOREIGN KEY(`campus_id`) REFERENCES `campus`(`campus_id`),
    FOREIGN KEY(`road_id`) REFERENCES `road`(`road_id`),
    FOREIGN KEY(`point_id_1`) REFERENCES `road_position_point`(`point_id`),
    FOREIGN KEY(`point_id_2`) REFERENCES `road_position_point`(`point_id`),
    CHECK (point_id_1 != point_id_2)
);