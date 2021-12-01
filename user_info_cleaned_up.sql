CREATE DATABASE user_info;
use user_info;

CREATE TABLE `User_Info` (
`User_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
`Name_User` varchar(50) NOT NULL,
`Email_Address` varchar(100) NOT NULL,
CONSTRAINT PK_UserID PRIMARY KEY (User_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER $$
-- I really don't know whether these 2 variables should have the same capacity as indicated in the column 
-- i halved the capacity i.e. for NameUser is defined as varchar(50) in column but in the SP as varchar(25)
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_user_info`(NameUser varchar(25), EmailAddress varchar(50))
BEGIN
    INSERT INTO User_Info (Name_User, Email_Address) VALUES (NameUser, EmailAddress);
END$$
DELIMITER ;

