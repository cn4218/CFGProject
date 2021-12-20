USE Products;
-- Creating the search results table
CREATE TABLE IF NOT EXISTS `search_results` (
-- after we get an MVP, can possible implement user/password
`Search_ID` INT NOT NULL UNIQUE AUTO_INCREMENT,
`User_ID` INT,
`List_Product_ID` MEDIUMTEXT  NOT NULL,
PRIMARY KEY(Search_ID));

-- This stored procedure called `fill_user_info` to create dummy data within our database
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `fill_search_table`(SearchID int, UserID int, ListProductID MEDIUMTEXT)
BEGIN
    INSERT INTO search_results (Search_ID, User_ID, List_Product_ID) VALUES (SearchID, UserID, ListProductID);
END$$
DELIMITER ;
