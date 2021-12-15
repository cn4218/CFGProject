import mysql.connector
from config import USER, PASSWORD, HOST

'''
Functions contained in this file:
_connect_to_db(db_name)
exception_handler(query)
exception_handler_wish(query)
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

"""
For Chizu:
I commented out my error messages because I've been struggling to connect to MySQL databases so I wanted to see the 
errors thrown without my printed error message
"""

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


# (query, error_message)
def exception_handler(query):
    """This function is the exception handler for exceptions that may arise when connecting to the
                    db  - it is a more general function"""

    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        cur.execute(query)
        db_connection.commit()
        cur.close()

    except mysql.connector.Error as e:
        print("Error code:"), e.errno  # error number
        print("SQLSTATE value:"), e.sqlstate  # SQLSTATE value
        print("Error message:"), e.msg  # error message
        print("Error:"), e  # errno, sqlstate, msg values
        s = str(e)
        print("Error:"), s  # errno, sqlstate, msg values

    # except Exception:
    #     raise DbConnectionError(error_message)
    # you pass whatever error message depending on the function that exception_handler is called within
    # eg of error messages could be "failure to insert data" , "failure to delete data"

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return


# (query, error_message)
def exception_handler_wish(query):
    """This function is the exception handler for exceptions that may arise when connecting to the
            db specifically for the wishlist functions"""

    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        cur.execute(query)

        result = (cur.fetchall())
        wish = _map_values(result)
        cur.close()

    except mysql.connector.Error as e:
        print("Error code:"), e.errno  # error number
        print("SQLSTATE value:"), e.sqlstate  # SQLSTATE value
        print("Error message:"), e.msg  # error message
        print("Error:"), e  # errno, sqlstate, msg values
        s = str(e)
        print("Error:"), s  # errno, sqlstate, msg values

    # except Exception:
    #     raise DbConnectionError(error_message)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return wish


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
It's really annoying to have all the parameters being passed as an argument but this is the only way to do it
You cannot pass another function or such into the argument for the add_wish_list function as it outside of the localised scope
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

# use the INSERT IGNORE command rather than the INSERT command. If a record doesn't duplicate an existing record, then MySQL inserts
# it as usual. If the record is a duplicate, then the IGNORE keyword tells MySQL to discard it silently without generating an error.

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
            VALUES ( {ProductID},
                           {Code_Wish},
                           '{Product_name}',   
                          '{Ingredients_Text}',  
                           '{Quantity}',   
                          '{Brands}',    
                          '{Brands_tags}', 
                          '{Categories}',
                          '{Categories_Tags}',   
                         '{Categories_En}', 
                           '{Countries}',    
                           '{Countries_Tags}',     
                           '{Countries_en}', 
                           '{Image_url}',      
                           '{Image_Small_url}',     
                           '{Image_Ingredients_url}',
                          '{Image_Ingredients_Small_url}',  
                           '{Image_Nutrition_url}',                     
                          '{Image_Nutrition_Small_url}', 
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
        Categories = Categories,
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

    exception_handler(query)

    display_statement = "Wishist item added for user with user ID {user_id}".format(
        user_id=UserID
    )

    print(display_statement)


# return info for a wishlist entry at a time
# need both user ID and product ID for the specific entry
def _get_wish_list_individual(UserID, ProductID):
    print('The User ID: {}. The Product ID: {}.'.format(UserID, ProductID))

    query = """ SELECT * FROM wish_list 
                 WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)

    error_message = "Failed to read data from DB"

    exception_handler_wish(query)


def _get_wish_list_all(UserID):
    print('The User ID: {}.'.format(UserID))

    query = """ SELECT * FROM wish_list 
                 WHERE User_ID = {} """.format(UserID)

    error_message = "Failed to read data from DB"

    exception_handler_wish(query)


'''
this function deletes an individual item from the wishlist
It takes the User ID, User Name and Product ID to find the unique user
'''
def delete_wishlist_item(UserID, ProductID):
    print('The User ID: {}. The Product ID: {}. to be deleted'.format(UserID, ProductID))

    query = """
                DELETE FROM Wish_List 
                WHERE User_ID = {} AND productID = {} """.format(UserID, ProductID)

    error_message = "Failed to read and subsequently delete data from DB"
    exception_handler(query)

    display_statement = (
        'The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}'.format(
            UserID, ProductID, {}))

    print(display_statement)

'''
This function deletes an entire wishlist associated with a user
It takes the User ID and User Name to find the unique user
'''
def delete_wishlist(UserID):
    print('The User ID: {}, to be deleted'.format(UserID))

    query = """
                DELETE FROM Wish_List 
                WHERE User_ID = {} 
                """.format(UserID)

    error_message = "Failed to read and subsequently delete data from DB"
    exception_handler(query)

    display_statement = (
        'The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}'.format(
            UserID, {}))

    print(display_statement)

'''
this function updates the wishlist for a record that has already been entered into the database
this function updates based on the user ID, username and product ID
'''
def update_wish_list(
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

    print('The User ID: {}.  The Product ID: {}.'.format(UserID, ProductID))
    query = """
                      UPDATE  wish_list
                      SET              

                      `productID` = {ProductID},
                      `code` = {Code_Wish},
                      `product_name` = '{Product_name}',
                      `ingredients_text` = '{Ingredients_Text}',
                      `quantity` = '{Quantity}',
                       `brands` = '{Brands}',
                       `brands_tags` = '{Brands_tags}',
                       'categories' = '{Categories}'
                       `categories_tags` = '{Categories_Tags}',
                       `categories_en` = '{Categories_En}',
                       `countries` = '{Countries}',
                       `countries_tags` = '{Countries_Tags}',
                       `countries_en` = '{Countries_en}',
                        `image_url` = '{Image_url}',
                        `image_small_url` = '{Image_Small_url}',
                        `image_ingredients_url` = '{Image_Ingredients_url}',
                         `image_ingredients_small_url` = '{Image_Ingredients_Small_url}',
                         `image_nutrition_url` = '{Image_Nutrition_url}',
                         `image_nutrition_small_url` = '{Image_Nutrition_Small_url}',
                         `User_ID` = {UserID}

                      WHERE `User_ID` = {UserID} AND  `productID` = {ProductID}
                      """.format(
        ProductID=ProductID,
        Code_Wish=Code_Wish,
        Product_name=Product_name,
        Ingredients_Text=Ingredients_Text,
        Quantity=Quantity,
        Brands=Brands,
        Brands_tags=Brands_tags,
        Categories = Categories,
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

    error_message = "Failed to red data and subsequently update records from DB"
    exception_handler(query)

