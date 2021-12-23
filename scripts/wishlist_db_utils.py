import mysql.connector
from mysql.connector import cursor

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from CFGProject.scripts.config import USER, PASSWORD, HOST


'''
FUNCTIONS CONTAINED IN THIS FILE:
_connect_to_db(db_name)
exception_handler(query, error_message)
exception_handler_wish(query, error_message)
exception_record_exists(query, error_message)
_map_values(result)

add_wish_list(
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
UserID
)

_get_wish_list_individual(UserID, ProductID)
_get_wish_list_all(UserID)
delete_wishlist_item(UserID, ProductID)
delete_wishlist(UserID)

'''


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    """
    This function takes the name of the MySQL database and forms a connection between Python and the database. The
    attempt to form the connection is executed through the use of a try-except block so that appropriate errors are able
    to be raised when a connection isn't able to be formed.
    It uses the mysql.connector package to generate the connection.
    Parameters
    -----------
    db_name: str
        Identifier to search the MySQL database to find the name of the database to form the connection. db_name is the
        name of the database.

    Returns
    --------
    cnx: mysql.connector.connection.MySQLConnection
        The connection created between Python and the MySQL workbench through the use of the mysql.connector package.

    Raises
    ------
    Exception
        The exception clause in the try-except block will raise an Error according to the Error module found in the
        mysql.connector package, whereby the different possible types of error raised are printed as appropriate.
    """
    try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin="mysql_native_password",
            database=db_name,
        )
        print("MySQL Database Connection is Successful")
        return cnx
    except mysql.connector.Error as e:
        print("Error code:"), e.errno  # error number
        print("SQLSTATE value:"), e.sqlstate  # SQLSTATE value
        print("Error message:"), e.msg  # error message
        print("Error:"), e  # errno, sqlstate, msg values
        s = str(e)
        print("Error:"), s  # errno, sqlstate, msg values


def exception_handler(query, error_message):
    """
    This function is the exception handler for exceptions that may arise when executing queries on the database. This
    function was written to fulfill DRY (Don't Repeat Yourself) as this code was used repeatedly throughout this file
    so I placed it to later execute queries with this function. It is a more general function so can be used with more
    queries relative to the other exception handler functions written.
    It uses the mysql.connector package to generate the connection.
    Parameters
    -----------
    query: str
        Query written to be executed against the database in MySQL workbench.

    error_message: str
        Error message to be returned when an exception is raised i.e. there is an issue connecting to the database.

    Returns
    --------
    Not applicable

    Raises
    ------
    Exception
        The exception clause in the try-except block will raise an Error according to the DbConnectionError class
        declared at the beginning of this file.
    """
    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)
        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception:
        raise DbConnectionError(error_message)
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return


def exception_handler_wish(query, error_message):
    """
    This function is the exception handler for exceptions that may arise when executing queries on the database. This
    function was written to fulfill DRY (Don't Repeat Yourself) as this code was used repeatedly throughout this file
    so I placed it to later execute queries with this function. This function is a more specific exception handler
    function relating to the wishlist functions as it returns the appropriate data in the form of a dictionary for
    the wishlist functions.
    It uses the mysql.connector package to generate the connection.
    Parameters
    -----------
    query: str
        Query written to be executed against the database in MySQL workbench.

    error_message: str
        Error message to be returned when an exception is raised i.e. there is an issue connecting to the database.

    Returns
    --------
        wish: list.
        This will return a list of dictionaries that are formatted to be relevant for the particular function e.g. for
        retrieving a wishlist for a unique user - it will return the entire wishlist in the form of a list of
        dictionaries for that unique user.


    Raises
    ------
    Exception
        The exception clause in the try-except block will raise an Error according to the DbConnectionError class
        declared at the beginning of this file.
    """
    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)
        cur.execute(query)
        result = (cur.fetchall())
        wish = _map_values(result)
        cur.close()
    except Exception:
        raise DbConnectionError(error_message)
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return wish


def exception_record_exists(query, error_message):
    """
    This function is the exception handler for exceptions that may arise when executing queries on the database. This
    function was written to fulfill DRY (Don't Repeat Yourself) as this code was used repeatedly throughout this file
    so I placed it to later execute queries with this function. This function is a more specific exception handler
    function relating checking if a record actually exists by running the appropriate query and counting the rows
    to determine whether the record exists on not in the MySQL database.
    It uses the mysql.connector package to generate the connection.
    Parameters
    -----------
    query: str
        Query written to be executed against the database in MySQL workbench.

    error_message: str
        Error message to be returned when an exception is raised i.e. there is an issue connecting to the database.

    Returns
    --------
        row_count: int
        This read-only property returns the number of rows returned for SELECT statements, or the number of rows
        affected by DML statements such as INSERT or UPDATE. This variable was used to determine whether a record
        existed or not according to what was the return value of row_count.


    Raises
    ------
    Exception
        The exception clause in the try-except block will raise an Error according to the DbConnectionError class
        declared at the beginning of this file.
    """
    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)
        cur.execute(query)
        result = (cur.fetchall())
        row_count = cur.rowcount
        cur.close()
    except Exception:
        raise DbConnectionError(error_message)
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return row_count


def _map_values(result):
    """
    This function used to map input data so that it will become a list of dictionaries that can be later presented to
    the user. This function serves to primarily create data that will formatted so the user is able to understand the
    data.
    Parameters
    -----------
    result: array
        Could be a list of lists or tuple of tuples.

    Returns
    --------
        mapped: list.
        This is used to later return a list of dictionaries that are formatted to be relevant for the particular
        function e.g. for retrieving a wishlist for a unique user - it will return the entire wishlist in the form of
        a list of dictionaries for that unique user.
    """
    mapped = []
    for item in result:
        mapped.append(
            {
                "productID": item[0],
                "code": item[1],
                "product_name": item[2],
                "ingredients_text": item[3],
                "quantity": item[4],
                "brands": item[5],
                "brands_tags": item[6],
                "categories": item[7],
                "categories_tags": item[8],
                "categories_en": item[9],
                "countries": item[10],
                "countries_tags": item[11],
                "countries_en": item[12],
                "image_url": item[13],
                "image_small_url": item[14],
                "image_ingredients_url": item[15],
                "image_ingredients_small_url": item[16],
                "image_nutrition_url": item[17],
                "image_nutrition_small_url": item[18],
                "User_ID": item[19],
            }
        )
    return mapped


def add_wish_list(
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
        UserID
):
    """
    This function is given input data as a list of variables. This list of variables was originally sent as a
    dictionary which was deconstructed in the app.py file. These variables are then added appropriately to the
    MySQL database in the wishlist table appropriately according to the UserID and ProductID.
    This function makes use of the INSERT IGNORE command rather than the INSERT command. If a record doesn't duplicate
    an existing record, then MySQL inserts it as usual. If the record is a duplicate, then the IGNORE keyword tells
    MySQL to discard it silently without generating an error.
    Parameters
    -----------
    ProductID: int
        Data retrieved from OBF database.

    Code_Wish: int
        Data retrieved from OBF database.

    Product_name: str
        Data retrieved from OBF database.

    Ingredients_Text: str
        Data retrieved from OBF database.

    Quantity: str
        Data retrieved from OBF database.

    Brands: str
        Data retrieved from OBF database.

    Brands_tags: str
        Data retrieved from OBF database.

    Categories: str
        Data retrieved from OBF database.

    Categories_Tags: str
        Data retrieved from OBF database.

    Categories_En: str
        Data retrieved from OBF database.

    Countries: str
        Data retrieved from OBF database.

    Countries_Tags: str
        Data retrieved from OBF database.

    Countries_en: str
        Data retrieved from OBF database.

    Image_url: str
        Data retrieved from OBF database.

    Image_Small_url: str
        Data retrieved from OBF database.

    Image_Ingredients_url: str
        Data retrieved from OBF database.

    Image_Ingredients_Small_url: str
        Data retrieved from OBF database.

    Image_Nutrition_url: str
        Data retrieved from OBF database.

    Image_Nutrition_Small_url: str
        Data retrieved from OBF database.

    UserID: int
        Data retrieved from OBF database.

    Returns
    --------
        Not applicable
    """
    query = """ INSERT IGNORE INTO wish_list (productID,
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
                ) 
                VALUES (  {ProductID},
                          {Code_Wish},
                         "{Product_name}",   
                         "{Ingredients_Text}",  
                         "{Quantity}",   
                         "{Brands}",    
                         "{Brands_tags}", 
                         "{Categories}",
                         "{Categories_Tags}",   
                         "{Categories_En}", 
                         "{Countries}",    
                         "{Countries_Tags}",     
                         "{Countries_en}", 
                         "{Image_url}",      
                         "{Image_Small_url}",     
                         "{Image_Ingredients_url}",
                         "{Image_Ingredients_Small_url}",  
                         "{Image_Nutrition_url}",                     
                         "{Image_Nutrition_Small_url}", 
                          {UserID}
                          )
                          """.format(
        ProductID=ProductID,
        Code_Wish=Code_Wish,
        Product_name=Product_name,
        Ingredients_Text=Ingredients_Text,
        Quantity=Quantity,
        Brands=Brands,
        Brands_tags=Brands_tags,
        Categories=Categories,
        Categories_Tags=Categories_Tags,
        Categories_En=Categories_En,
        Countries=Countries,
        Countries_Tags=Countries_Tags,
        Countries_en=Countries_en,
        Image_url=Image_url,
        Image_Small_url=Image_Small_url,
        Image_Ingredients_url=Image_Ingredients_url,
        Image_Ingredients_Small_url=Image_Ingredients_Small_url,
        Image_Nutrition_url=Image_Nutrition_url,
        Image_Nutrition_Small_url=Image_Nutrition_Small_url,
        UserID=UserID
    )

    error_message = "Failure to insert data into DB"
    exception_handler(query, error_message)
    display_statement = "Wishlist item added for user with user ID {user_id}".format(
        user_id=UserID
    )

    print(display_statement)


def _get_wish_list_individual(UserID, ProductID):
    """
    This function is used to retrieve the unique wishlist item for a particular based on the UserID and ProductID
    parameters. It will fetch the relevant row in the wishlist table in the MySQL database and thus display it to the
    user in a readable format.
    Parameters
    -----------
    UserID: int
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    ProductID: str
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    Returns
    --------
        display_statement: str
        This variable is returned to the user in the situation where the record they are attempting to retrieve does
        not exist. It will return a display statement which is a readable statement for the user stating that that
        particular record does not exist.

        result: array
        This could be a list of lists or tuple of tuples. If the query has run successfully, it will fetch the result
        from the wishlist table in the MySQL database which will display the wishlist item for the user in a readable
        format.
    """
    query = """ SELECT * FROM wish_list WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)
    error_message = "Failed to read data from DB"
    result = exception_handler_wish(query, error_message)
    if result == []:
        display_statement = "Wish list item for User_ID = {} and " \
                            "productID = {} does not exist """.format(UserID, ProductID)
        return display_statement
    elif result != []:
        return result
    return


def _get_wish_list_all(UserID):
    """
    This function is used to retrieve the entire wishlist for a particular based on the UserID parameter. It will fetch
    the relevant rows in the wishlist table in the MySQL database and thus display it to the user in a readable format.
    Parameters
    -----------
    UserID: int
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    Returns
    --------
        display_statement: str
        This variable is returned to the user in the situation where the record they are attempting to retrieve does
        not exist. It will return a display statement which is a readable statement for the user stating that that
        particular user does not yet have a wishlist.

        result: array
        This could be a list of lists or tuple of tuples. If the query has run successfully, it will fetch the result
        from the wishlist table in the MySQL database which will display the entire wishlist for the user in a readable
        format.
    """
    query = """ SELECT * FROM wish_list WHERE User_ID = {} """.format(UserID)
    error_message = "Failed to read data from DB"
    result = exception_handler_wish(query, error_message)
    if result == []:
        display_statement = "Wish list User_ID = {} is empty """.format(UserID)
        return display_statement
    elif result != []:
        return result
    return


def delete_wishlist_item(UserID, ProductID):
    """
    This function is used to delete an unique wishlist item for a particular based on the UserID and ProductID
    parameters. It will delete the relevant row in the wishlist table in the MySQL database and thus display this action
    to the user in a readable format.
    Parameters
    -----------
    UserID: int
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    ProductID: str
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    Returns
    --------
        display_statement: str
        This variable is returned to the user in the situation where the record they are attempting to delete does
        not exist. It will return a display statement which is a readable statement for the user stating that that
        particular record does not exist.

        result: array
        This could be a list of lists or tuple of tuples. If the query has run successfully, it will fetch the result
        of the command of deleting the wishlist item for that particular user from the wishlist table in the MySQL
        database which will present the deletion of the record for the user in a readable format.
    """
    query = """ SELECT * FROM wish_list WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)
    error_message = "Error"
    row_count = exception_handler_wish(query, error_message)
    if row_count == []:
        display_statement = ("Wishlist item for User_ID: {} and "
                             "productID: {} does not exist").format(UserID, ProductID)
    elif row_count != []:
        query = """ DELETE FROM wish_list WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)
        error_message = "Failed to read and subsequently delete data from DB"
        exception_handler(query, error_message)
        display_statement = (
            "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. "
            "This wishlist record is now empty: {}".format(
                UserID, ProductID, {}))
    return display_statement


def delete_wishlist(UserID):
    """
    This function is used to delete an entire wishlist for a particular based on the UserID parameter. It will delete
    the relevant rows in the wishlist table in the MySQL database and thus display this action to the user in a readable
    format.
    -----------
    UserID: int
        Identifier to find the appropriate row (wishlist item) in the wishlist table in the MySQL database.

    Returns
    --------
        display_statement: str
        This variable is returned to the user in the situation where the records they are attempting to delete does
        not exist. It will return a display statement which is a readable statement for the user stating that that
        wishlist for that particular user does not exist.

        result: array
        This could be a list of lists or tuple of tuples. If the query has run successfully, it will fetch the result
        of the command of deleting the entire wishlist for that particular user from the wishlist table in the MySQL
        database which will present the deletion of the records for the user in a readable format.
    """
    query = """ SELECT * FROM wish_list WHERE User_ID = {} """.format(UserID)
    error_message = "Error"
    row_count = exception_handler_wish(query, error_message)
    if row_count == []:
        display_statement = "Wishlist item for this User_ID: {} does not exist".format(UserID)
    elif row_count != []:
        query = """
                DELETE FROM wish_list 
                WHERE User_ID = {} """.format(UserID)

        error_message = "Failed to read and subsequently delete data from DB"

        exception_handler(query, error_message)

        display_statement = (
            "The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}".format(
                UserID, {}))
    return display_statement
