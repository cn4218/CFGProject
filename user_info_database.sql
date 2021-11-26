-- remember mysql is case insenstive
CREATE DATABASE user_info;
use user_info;

-- remember when entering names such as table to use ` (located next to 1) and not ' 
CREATE TABLE `User_Info` (
`Name` varchar(50) NOT NULL
) ;

ALTER TABLE user_info
-- COLUMN keyword is optional but i added it for readability
-- after keyword means that this column is placed after name
ADD COLUMN `Email_Address` varchar(100) NOT NULL AFTER `Name`;

ALTER TABLE user_info
-- when using FIRST, do not put a column name after it!!! will throw errors. First is to be used to create the very first column.
ADD COLUMN `User_ID` int NOT NULL FIRST;

ALTER TABLE user_info
-- add the following constraint so that all the values in the user id column are unique
ADD UNIQUE (User_ID);

select * from user_info;

-- I submitted a doc so people could have a look but I'm currently working on trying to generate a random user ID, sorry if itakes 
-- time, I'm not the best with MySQL so wanted to practice with this task hehe

