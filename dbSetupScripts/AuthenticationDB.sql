-- Database for : Authentication
-- Contributors: Edwin Garcia, Andrew Herbst, Duc Tran

-- 1. drop the database AUTHENTICATION if it exists
-- 2. create the database Authentication
-- 3. set the current DB context to the newly created database, and then execute the DDL statements.

SET foreign_key_checks = 0;


drop database if exists AUTHENTICATION;
create database AUTHENTICATION;
use AUTHENTICATION;

SET autocommit=0; 
-- disables auto commit

-- Table structure for table `authentication`

DROP TABLE IF EXISTS authentication;

CREATE TABLE authentication (
  username varchar(20)	NOT NULL,
  hashkey  int(11)     	NOT NULL,
  initPw   char		NOT NULL,
  dbID	   int		NOT NULL AUTO_INCREMENT, 	
  PRIMARY KEY (dbID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- Auto_Increment ID. Starts at 1. So to do insert command, no need to add dbID value since it auto increments


start transaction;

INSERT INTO authentication (username, hashkey, initPw) 
VALUES ("airsound",39,"a"),("db1",16,"t");

commit;
-- must include name of columns(except dbID) since we are auto incrementing
-- automatically rollback if error occurs
-- notice no need to add dbID value since dbID auto increments
-- inputing hashkey value from what I got from the hashkey function in the hashkey.py file

SET foreign_key_checks = 1;




