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

-- this stored procedure called `fill_user_info` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_user_info`(UserName varchar(50), NameUser varchar(50), EmailAddress varchar(100))
BEGIN
-- Use the INSERT IGNORE command rather than the INSERT command. If a record doesn't duplicate an existing record, then MySQL inserts
-- it as usual. If the record is a duplicate, then the IGNORE keyword tells MySQL to discard it silently without generating an error.
    INSERT IGNORE INTO User_Info (User_Name, Name_User, Email_Address) VALUES (UserName, NameUser, EmailAddress);
END$$
DELIMITER ;

-- creating the wish list table

CREATE TABLE if not exists  `Wish_List` (
`User_ID` int,
`User_Name` varchar(50),
`productID` INTEGER,
`code` MEDIUMTEXT NULL,
`product_name` VARCHAR(500) NULL,
`quantity` VARCHAR(100) NULL,
`brands` VARCHAR(500) NULL,
`brands_tags` VARCHAR(500) NULL,
`categories_tags` VARCHAR(500) NULL,
`categories_en` VARCHAR(500) NULL,
`countries` VARCHAR(500) NULL,
`countries_tags` VARCHAR(500) NULL,
`countries_en` VARCHAR(500) NULL,
`ingredients_text` VARCHAR(1000) NULL,
`image_url` VARCHAR(1000) NULL,
`image_small_url` VARCHAR(1000) NULL,
`image_ingredients_url` VARCHAR(1000) NULL,
`image_ingredients_small_url` VARCHAR(1000) NULL,
`image_nutrition_url` VARCHAR(1000) NULL,
`image_nutrition_small_url` VARCHAR(1000) NULL,
FOREIGN KEY (User_ID) REFERENCES User_Info(User_ID),
FOREIGN KEY (User_Name) REFERENCES User_Info(User_Name),
CONSTRAINT PK_User PRIMARY KEY (User_Name, User_ID, productID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- this stored procedure called `fill_wish_list` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_wish_list`(
UserID INT, 
UserName varchar(50), 
ProductID INTEGER, 
Code_Wish MEDIUMTEXT, 
Product_name VARCHAR(500),
Quantity VARCHAR(100), 
Brands VARCHAR(500), 
Brands_tags VARCHAR(500), 
Categories_Tags VARCHAR(500), 
Categories_En VARCHAR(500),
Countries VARCHAR(500),
Countries_Tags VARCHAR(500),
Countries_en VARCHAR(500), 
Ingredients_Text VARCHAR(1000), 
Image_url VARCHAR(1000), 
Image_Small_url VARCHAR(1000), 
Image_Ingredients_url VARCHAR(1000), 
Image_Ingredients_Small_url VARCHAR(1000), 
Image_Nutrition_url VARCHAR(1000), 
Image_Nutrition_Small_url VARCHAR(1000)
)
BEGIN
    INSERT INTO Wish_List (
    User_ID, 
    User_Name,
    productID, 
    code, 
    product_name, 
    quantity, 
    brands, 
    brands_tags, 
    categories_tags, 
    categories_en, 
    countries, 
    countries_tags, 
    countries_en, 
    ingredients_text, 
    image_url, 
    image_small_url, 
    image_ingredients_url, 
    image_ingredients_small_url, 
    image_nutrition_url, 
    image_nutrition_small_url) VALUES (
    UserID, 
    UserName,
    ProductID, 
    Code_Wish, 
    Product_name, 
    Quantity, 
    Brands, 
    Brands_tags, 
    Categories_Tags, 
    Categories_En, 
    Countries, 
    Countries_Tags, 
    Countries_en, 
    Ingredients_Text, 
    Image_url, 
    Image_Small_url, 
    Image_Ingredients_url, 
    Image_Ingredients_Small_url, 
    Image_Nutrition_url, 
    Image_Nutrition_Small_url);
END$$
DELIMITER ;

