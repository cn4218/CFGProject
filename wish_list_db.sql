CREATE DATABASE wish_list;
use wish_list;

CREATE TABLE `Wish_List` (
`User_ID` int NOT NULL,
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
CONSTRAINT PK_UserID PRIMARY KEY (User_ID, productID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_wish_list`(
UserID INT, 
ProductID INTEGER, 
Code_Wish MEDIUMTEXT, 
Product_name VARCHAR(500),
Quantity VARCHAR(100), 
Brands VARCHAR(500), 
Brands_tags VARCHAR(500), 
Categories_Tags VARCHAR(500), 
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
    image_nutrition_small_url) VALUES (UserID, ProductID, Code_Wish, Product_name, Quantity, 
    Brands, Brands_tags, Categories_Tags, Categories_En, Countries, Countries_Tags, Countries_en, Ingredients_Text, Image_url, 
    Image_Small_url, Image_Ingredients_url, Image_Ingredients_Small_url, Image_Nutrition_url, Image_Nutrition_Small_url);
END$$
DELIMITER ;

