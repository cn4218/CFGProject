import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    try:    ##change: added try
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


# lord only know if i even need this function , as i have later updated the MySQL database with a seperate function
# im following lesson 20 and im a bit confused
def _map_values(result):
    mapped = []
    for item in result:
        mapped.append(
            {
                "User_ID": item[0],
                "User_Name": item[1],
                "productID": item[2],
                "code": item[3],
                "product_name": item[4],
                "quantity": item[5],
                "brands": item[6],
                "brands_tags": item[7],
                "categories_tags": item[8],
                "categories_en": item[9],
                "countries": item[10],
                "countries_tags": item[11],
                "countries_en": item[12],
                "ingredients_text": item[13],
                "image_url": item[14],
                "image_small_url": item[15],
                "image_ingredients_url": item[16],
                "image_ingredients_small_url": item[17],
                "image_nutrition_url": item[18],
                "image_nutrition_small_url": item[19],
            }
        )
    return mapped




# return info for a wishlist entry at a time
# need both user ID and product ID for the specific entry
def _get_wish_list_individual(UserID, ProductID):   # dont need username
    print('The User ID: {}.  The Product ID: {}.'.format(UserID, ProductID))
    try:
        db_name = "cfg_project"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM wish_list 
         WHERE User_ID = '{}' AND productID = '{}' """.format(UserID, ProductID)

        cur.execute(query)

        result = (cur.fetchall())
        wish = _map_values(result)
        cur.close()
    except Exception as Error:
        print(Error)   ##change: as error
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return wish

def _get_wish_list_all(UserID):   # do we need username
    print('The User ID: {}'.format(UserID))
    try:
        db_name = "cfg_project"   ## change db name
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM wish_list 
         WHERE User_ID = '{}'""".format(UserID)

        cur.execute(query)

        result = (cur.fetchall())
        wishlist = _map_values(result)
        cur.close()
    except Exception as Error:
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return wishlist


'''
this function deletes an individual item from the wishlist
It takes the User ID, User Name and Product ID to find the unique user
'''
def delete_wishlist_item(UserID, ProductID):
    print('The User ID: {}.  The Product ID: {}. to be deleted'.format(UserID, ProductID))
    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        DELETE FROM Wish_List 
        WHERE User_ID = '{}' AND productID = '{}' """.format(UserID, ProductID)

        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)
    finally:
        if db_connection:
            db_connection.close()
            # print("The new resultant wishlist for this user with User ID: {}. is: {}".format(UserID, _get_wish_list_all(UserID))"")
    return {}

'''
This function deletes an entire wishlist associated with a user
It takes the User ID and User Name to find the unique user
'''
def delete_wishlist(UserID):
    print('The User ID: {}. . to be deleted'.format(UserID)) ##change: deleteed productid
    try:
        db_name = 'cfg_project'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        DELETE FROM Wish_List 
        WHERE User_ID = '{}';
        """.format(UserID)

        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)
    finally:
        if db_connection:
            db_connection.close()
    return {}


