/*
 Lily Kendall
 Database HW 3
 Due 9/25/24
 */

 -- Part 2: problems

DROP DATABASE IF EXISTS klkend22_insurance;
CREATE DATABASE klkend22_insurance;

 -- 3.13: Write SQL DDL corresponding to the schema in Figure 3.17. Make any reasonable assumptions about data types,
-- and be sure to declare primary and foreign keys.

-- fig. 3.17 :
-- person (driver id, name, address)
-- car (license plate, model, year)
-- accident (report number, year, location)
-- owns (driver id, license plate)
-- participated (report number, license plate, driver id, damage amount)

 CREATE TABLE person (
     driver_id varchar(8),
     name varchar(20),
     address varchar(50),
     PRIMARY KEY (driver_id)
 );

 CREATE TABLE car (
     license_plate varchar(8),
     model varchar(20),
     year int,
     PRIMARY KEY (license_plate)
 );

CREATE TABLE accident (
    report_number varchar(8),
    year int,
    location varchar(20),
    PRIMARY KEY (report_number)
);

CREATE TABLE owns (
    driver_id varchar(8),
    license_plate varchar(8),
    PRIMARY KEY (driver_id, license_plate),
    FOREIGN KEY (driver_id) REFERENCES person (driver_id),
    FOREIGN KEY (license_plate) REFERENCES car (license_plate)
);

CREATE TABLE participated (
    report_number varchar(20),
    license_plate varchar(8),
    driver_id varchar(8),
    damage_amount float,
    PRIMARY KEY (report_number, license_plate),
    FOREIGN KEY (report_number) REFERENCES accident(report_number),
    FOREIGN KEY (license_plate) REFERENCES car(license_plate),
    FOREIGN KEY (driver_id) REFERENCES person(driver_id)
);

-- 3.14 Consider the insurance database of Figure 3.17, where the primary keys are
-- underlined. Construct the following SQL queries for this relational database.

-- a: Find the number of accidents involving a car belonging to a person named “John Smith”.

SELECT count(*)
FROM participated
WHERE driver_id = (SELECT driver_id FROM person WHERE name = 'John Smith'); -- using a subquery to get the driver_id of John Smith

-- b: Update the damage amount for the car with license plate “AABB2000”
-- in the accident with report number “AR2197” to $3000.

UPDATE participated
SET damage_amount = 3000 -- setting the damage amount to 3000
WHERE license_plate = 'AABB2000' AND report_number = 'AR2197'; -- find the correct row to update

