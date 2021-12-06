CREATE DATABASE Products;
USE Products;

CREATE TABLE products_table(
    productID INTEGER PRIMARY KEY,
    code MEDIUMTEXT NULL,
    product_name VARCHAR(500) NULL,
    ingredients_text VARCHAR(1000) NULL,
    quantity VARCHAR(100) NULL,
    brands VARCHAR(500) NULL,
    brands_tags VARCHAR(500) NULL,
    categories_tags VARCHAR(500) NULL,
    categories_en VARCHAR(500) NULL,
    countries VARCHAR(500) NULL,
    countries_tags VARCHAR(500) NULL,
    countries_en VARCHAR(500) NULL,
    image_url VARCHAR(1000) NULL,
    image_small_url VARCHAR(1000) NULL,
    image_ingredients_url VARCHAR(1000) NULL,
    image_ingredients_small_url VARCHAR(1000) NULL,
    image_nutrition_url VARCHAR(1000) NULL,
    image_nutrition_small_url VARCHAR(1000) NULL
);


SELECT * 
FROM products_table;

/*
STORED PROCEDURE to insert data from products_table.csv (TABLE Ab) CSV file
into Products.products_table SQL table
*/
DELIMITER $$
CREATE DEFINER='root'@'localhost' PROCEDURE fillproducts(
    productID INTEGER,
    code MEDIUMTEXT,
    product_name VARCHAR(500),
    ingredients_text VARCHAR(1000),
    quantity VARCHAR(100),
    brands VARCHAR(500),
    brands_tags VARCHAR(500),
    categories_tags VARCHAR(500),
    categories_en VARCHAR(500),
    countries VARCHAR(500),
    countries_tags VARCHAR(500),
    countries_en VARCHAR(500),
    image_url VARCHAR(1000),
    image_small_url VARCHAR(1000),
    image_ingredients_url VARCHAR(1000),
    image_ingredients_small_url VARCHAR(1000),
    image_nutrition_url VARCHAR(1000),
    image_nutrition_small_url VARCHAR(1000)
)
BEGIN
	INSERT INTO products_table (
        productID,
        code,
        product_name,
        ingredients_text,
        quantity,
        brands,
        brands_tags,
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
        image_nutrition_small_url
	) 
	VALUES (
        productID,
        code,
        product_name,
        ingredients_text,
        quantity,
        brands,
        brands_tags,
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
        image_nutrition_small_url
	);
END$$
DELIMITER ;

/*
STORED PROCEDURE to get products containing ingredients from Products.products_table SQL table
*/
DELIMITER $$
CREATE PROCEDURE getproduct(ingredient)
BEGIN
SELECT productID, product_name, ingredients_text
FROM products_table
WHERE ingredient IN ingredients_text;
END$$
DELIMITER ;


