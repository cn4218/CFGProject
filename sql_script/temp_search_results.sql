use products;
-- creating the search results table
CREATE TABLE if not exists  `search_results` (
-- after we get an MVP, can possible implement user/password
`Search_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
`List_Product_ID` MEDIUMTEXT  NOT NULL,
PRIMARY KEY(Search_ID));


-- this stored procedure called `fill_user_info` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_search_table`(SearchID int,  ListProductID MEDIUMTEXT)
BEGIN
    INSERT INTO search_results (Search_ID, List_Product_ID) VALUES (SearchID, ListProductID);
END$$
DELIMITER ;

CALL `products`.`fill_search_table`(1, '{"product_ids": list_of_products_dummy_data}');