CREATE DATABASE user_info;
use user_info;

CREATE TABLE `User_Info` (
`User_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
`Name` varchar(50) NOT NULL,
`Email_Address` varchar(100) NOT NULL,
CONSTRAINT PK_UserID PRIMARY KEY (User_ID)
) ;