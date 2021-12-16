/* Test database to check info from html form is being sent to sql db *\
CREATE DATABASE Test;
USE Test;
CREATE TABLE Testing (
	name VARCHAR(55),
	username VARCHAR(55),
	password VARCHAR(55),
	email VARCHAR(55)
);

SELECT*FROM Testing;
