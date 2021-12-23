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

update_wish_list(
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
'''


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
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
    This function is the exception handler for exceptions that may arise when
    connecting to the database — it is a more general function
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
    This function is the exception handler for exceptions that may arise when
    connecting to the database — specifically for the wishlist functions
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



'''
Use the INSERT IGNORE command rather than the INSERT command. If a record doesn't duplicate an existing record, then 
MySQL inserts it as usual. If the record is a duplicate, then the IGNORE keyword tells MySQL to discard it silently
without generating an error.
'''


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

    display_statement = "Wishist item added for user with user ID {user_id}".format(
        user_id=UserID
    )

    print(display_statement)


# returns info for a wishlist entry at a time
# need both user ID and product ID for the specific entry
def _get_wish_list_individual(UserID, ProductID):

    query = """ SELECT * FROM wish_list 
                 WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)

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
    This function deletes an individual item from the wishlist
    It takes the User ID, User Name and Product ID to find the unique user
    """

    query = """
       SELECT * FROM wish_list WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)

    error_message = "Error"

    row_count = exception_handler_wish(query, error_message)

    if row_count == []:
        display_statement = ("Wishlist item for User_ID: {} and "
                             "productID: {} does not exist").format(UserID, ProductID)

    elif row_count != []:
        query = """
                   DELETE FROM wish_list 
                   WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)

        error_message = "Failed to read and subsequently delete data from DB"

        exception_handler(query, error_message)

        display_statement = (
            "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. "
            "This wishlist record is now empty: {}".format(
                UserID, ProductID, {}))
    return display_statement



def delete_wishlist(UserID):
    """
    This function deletes an entire wishlist associated with a user
    It takes the User ID and User Name to find the unique user
    """

    query = """
    SELECT * FROM wish_list WHERE User_ID = {} """.format(UserID)

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

