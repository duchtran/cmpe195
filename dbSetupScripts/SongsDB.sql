-- Database for : 1
-- Contributors: Edwin Garcia, Andrew Herbst, Duc Tran

-- 1. drop the database db1 if it exists
-- 2. create the database db1
-- 3. set the current DB context to the newly created database, and then execute the DDL statements.
-- so the database name is called db1

SET foreign_key_checks = 0;


drop database if exists db1;
create database db1;
use db1;

SET autocommit=0; 
-- disables auto commit

-- creating table structures


CREATE TABLE genre (
  name     varchar(255) 		NOT NULL,
  PRIMARY KEY(name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE author (
  name     varchar(255) 		NOT NULL,
  PRIMARY KEY(name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE artist (
  name     varchar(255) 		NOT NULL,
  PRIMARY KEY(name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE category (
  name     varchar(255) 		NOT NULL,
  songID   int	 				NOT NULL,
  PRIMARY KEY(name,songID),
  FOREIGN KEY(songID) REFERENCES songs(songID)
	ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(name) REFERENCES genre(name)
	ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE belongs_to (
  name     varchar(255) 		NOT NULL,
  songID   int	 				NOT NULL,
  PRIMARY KEY(name,songID),
  FOREIGN KEY(name) REFERENCES author(name)
	ON UPDATE CASCADE ON DELETE CASCADE,	
  FOREIGN KEY(songID) REFERENCES songs(songID)
	ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE performed_by (
  name     varchar(255) 		NOT NULL,
  songID   int	 				NOT NULL,
  PRIMARY KEY(name,songID),
  FOREIGN KEY(name) REFERENCES artist(name)
	ON UPDATE CASCADE ON DELETE CASCADE,	
  FOREIGN KEY(songID) REFERENCES songs(songID)
	ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE songs (
  songID   int	 				NOT NULL AUTO_INCREMENT,
  name     varchar(255) 		NOT NULL,
  URL   char(1) 				NOT NULL,
  PRIMARY KEY (songID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- Auto_Increment ID. Starts at 1. So to do insert command, no need to add songID value since it auto increments




start transaction;

INSERT INTO songs
	(name,URL)
	VALUES	("Fools Gold",					"www.worldstarhiphop.com"),
			("La Bamba", 					"www.youtube.com"),
			("Ill Be Home For Christmas", 	"www.google.com");

commit;
-- must include name of columns(except songID) since we are auto incrementing
-- automatically rollback if error occurs
-- notice no need to add songID value since songID auto increments
-- inputing hashkey value from what I got from the hashkey function in the hashkey.py file



start transaction;

INSERT INTO category
	(name,songID)
	VALUES	("Hip Hop", 		1),
			("Rock and Roll", 	2),
			("Holiday", 		3);

commit;


start transaction;

INSERT INTO belongs_to
	(name,songID)
	VALUES	("Andy Mineo", 		1),
			("Ritchie Valens", 	2),
			("Frank Sinatra", 	3);

commit;

start transaction;

INSERT INTO performed_by
	(name,songID)
	VALUES	("Andy Mineo", 		1),
			("Sho Baraka", 		1),
			("Swoope", 			1),
			("Ritchie Valens", 	2),
			("Frank Sinatra", 	3);

commit;


start transaction;

INSERT INTO genre
	(name)
	VALUES	("Hip Hop"),
			("Rock and Roll"),
			("Holiday");

commit;


start transaction;

INSERT INTO author
	(name)
	VALUES	("Andy Mineo"),
			("Ritchie Valens"),
			("Frank Sinatra");

commit;


start transaction;

INSERT INTO artist
	(name)
	VALUES	("Andy Mineo"),
			("Sho Baraka"),
			("Swoope"),
			("Ritchie Valens"),
			("Frank Sinatra");

commit;

SET foreign_key_checks = 1;




