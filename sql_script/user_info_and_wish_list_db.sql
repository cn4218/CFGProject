CREATE DATABASE if not exists CFG_Project;
use CFG_Project;

-- creating the user info table
CREATE TABLE if not exists  `User_Info` (
-- after we get an MVP, can possible implement user/password
`User_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
`User_Name` varchar(50) UNIQUE NOT NULL,
`Name_User` varchar(50) NOT NULL,
`Email_Address` varchar(100) NOT NULL,
-- In this statement, you can also use the UNIQUE INDEX instead of the UNIQUE KEY because they are synonyms.
-- When you create a UNIQUE constraint, MySQL creates a UNIQUE index behind the scenes.
-- UNIQUE KEY line is to prevent duplicate records, the combination of User_ID, User_Name, Name_User should produce a unique record
-- unique_user is the name I gave to the key
UNIQUE KEY unique_user (User_ID, User_Name, Name_User),
CONSTRAINT PK_User PRIMARY KEY (User_Name, User_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Need to have one line as dummy data so the instructor will be able to login 
INSERT IGNORE INTO User_Info (User_ID, User_Name, Name_User, Email_Address) VALUES (10234, 'sample_name', 'sample_user','sample@gmail.com');


-- this stored procedure called `fill_user_info` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_user_info`(UserID int, UserName varchar(50), NameUser varchar(50), EmailAddress varchar(100))
BEGIN
-- Use the INSERT IGNORE command rather than the INSERT command. If a record doesn't duplicate an existing record, then MySQL inserts
-- it as usual. If the record is a duplicate, then the IGNORE keyword tells MySQL to discard it silently without generating an error.
    INSERT IGNORE INTO User_Info (User_ID, User_Name, Name_User, Email_Address) VALUES (UserID, UserName, NameUser, EmailAddress);
END$$
DELIMITER ;

-- creating the wish list table

CREATE TABLE if not exists  `Wish_List` (
`productID` INTEGER,
`code` BIGINT NULL,
`product_name` VARCHAR(500) NULL,
`ingredients_text` VARCHAR(1000) NULL,
`quantity` VARCHAR(100) NULL,
`brands` VARCHAR(500) NULL,
`brands_tags` VARCHAR(500) NULL,
`categories` VARCHAR(500) NULL,
`categories_tags` VARCHAR(500) NULL,
`categories_en` VARCHAR(500) NULL,
`countries` VARCHAR(500) NULL,
`countries_tags` VARCHAR(500) NULL,
`countries_en` VARCHAR(500) NULL,
`image_url` VARCHAR(1000) NULL,
`image_small_url` VARCHAR(1000) NULL,
`image_ingredients_url` VARCHAR(1000) NULL,
`image_ingredients_small_url` VARCHAR(1000) NULL,
`image_nutrition_url` VARCHAR(1000) NULL,
`image_nutrition_small_url` VARCHAR(1000) NULL,
`User_ID` int,
FOREIGN KEY (User_ID) REFERENCES User_Info(User_ID),
CONSTRAINT PK_User PRIMARY KEY (User_ID, productID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- this stored procedure called `fill_wish_list` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_wish_list`(
ProductID INTEGER,
Code_Wish BIGINT,
Product_name VARCHAR(500),
Ingredients_Text VARCHAR(1000),
Quantity VARCHAR(100),
Brands VARCHAR(500),
Brands_tags VARCHAR(500),
Categories VARCHAR(500),
Categories_Tags VARCHAR(500),
Categories_En VARCHAR(500),
Countries VARCHAR(500),
Countries_Tags VARCHAR(500),
Countries_en VARCHAR(500),
Image_url VARCHAR(1000),
Image_Small_url VARCHAR(1000),
Image_Ingredients_url VARCHAR(1000),
Image_Ingredients_Small_url VARCHAR(1000),
Image_Nutrition_url VARCHAR(1000),
Image_Nutrition_Small_url VARCHAR(1000),
UserID int
)
BEGIN
    INSERT IGNORE INTO Wish_List (
productID,
code,
product_name,
ingredients_text,
quantity,
brands,
brands_tags,
categories,
categories_tags,
categories_en,
countries,
countries_tags,
countries_en,
image_url,
image_small_url,
image_ingredients_url,
image_ingredients_small_url,
image_nutrition_url,
image_nutrition_small_url,
User_ID
) VALUES (
ProductID,
Code_Wish,
Product_name,
Ingredients_Text,
Quantity,
Brands,
Brands_tags,
Categories,
Categories_Tags,
Categories_En,
Countries,
Countries_Tags,
Countries_en,
Image_url,
Image_Small_url,
Image_Ingredients_url,
Image_Ingredients_Small_url,
Image_Nutrition_url,
Image_Nutrition_Small_url,
UserID);
END$$
DELIMITER ;

