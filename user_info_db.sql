CREATE DATABASE user_info;
use user_info;

CREATE TABLE `User_Info` (
-- after we get an MVP, can possible implement user/password
`User_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
`User_Name` varchar(50) NOT NULL,
`Name_User` varchar(50) NOT NULL,
`Email_Address` varchar(100) NOT NULL,
CONSTRAINT PK_User PRIMARY KEY (User_Name, User_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_user_info`(UserName varchar(50), NameUser varchar(50), EmailAddress varchar(100))
BEGIN
    INSERT INTO User_Info (User_Name, Name_User, Email_Address) VALUES (UserName, NameUser, EmailAddress);
END$$
DELIMITER ;

