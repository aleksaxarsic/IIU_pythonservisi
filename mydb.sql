 CREATE DATABASE mydb;

 USE mydb;

 CREATE TABLE services (
   id INT NOT NULL AUTO_INCREMENT,
   name VARCHAR(255) NOT NULL,
   description VARCHAR(255),
   PRIMARY KEY (id)
 );