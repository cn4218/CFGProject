import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=db_name,
    )
    print("MySQL Database Connection is Successful")
    except mysql.connector.Error as e:
    print("Error code:"), e.errno  # error number
    print("SQLSTATE value:"), e.sqlstate  # SQLSTATE value
    print("Error message:"), e.msg  # error message
    print("Error:"), e  # errno, sqlstate, msg values
    s = str(e)
    print("Error:"), s  # errno, sqlstate, msg values
    return cnx

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
                "quantity": item[5]
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

'''
It's really annoying to have all the parameters being passed as an argument but this is the only way to do it
You cannot pass another function or such into the argument for the add_wish_list function as it outside of the localised scope
'''

def add_wish_list(UserID, UserName, ProductID, Code_Wish, Product_name, Quantity,
    Brands, Brands_tags, Categories_Tags, Countries_en, Ingredients_Text, Image_url, Image_Small_url, Image_Ingredients_url,
    Image_Ingredients_Small_url, Image_Nutrition_url, Image_Nutrition_Small_url):
    try:
        db_name = "wish_list"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ INSERT INTO wish_list ({User_ID},
         {User_Name},
        {productID},
        {code},
        {product_name},
        {quantity},
         {brands}, 
        {brands_tags},
        {categories_tags},
        {categories_en},
        {countries},
        {countries_tags},
        {countries_en},
        {ingredients_text},
        {image_url},
        {image_small_url},
         {image_ingredients_url},
         {image_ingredients_small_url},
        {image_nutrition_url},
        {image_nutrition_small_url}
        ) 
        VALUES ( '{UserID}',
                       '{UserName}',
                       '{ProductID}',
                      '{Code_Wish}',
                       '{Product_name}',
                      '{Quantity}',
                      '{Brands}',
                      ` '{Brands_tags}',
                     '{Categories_Tags}',
                       '{Categories_En}',
                       '{Countries}',
                       '{Countries_Tags}',
                       '{Countries_en}',
                       '{Ingredients_Text}',
                       '{Image_url}',
                      '{Image_Small_url}',
                       '{Image_Ingredients_url}',
                      '{Image_Ingredients_Small_url}', 
                       '{Image_Nutrition_url}', 
                       '{Image_Nutrition_Small_url}'
                  )
                  """.format(
            User_ID = User_ID,
            UserID = UserID,
            User_Name = User_Name,
            UserName = UserName,
            productID = productID,
            ProductID = ProductID,
            code = code,
            Code_Wish = Code_Wish,
            product_name = product_name,
            Product_name = Product_name,
            quantity = quantity,
            Quantity = Quantity,
            brands = brands,
            Brands = Brands,
            brands_tags = brands_tags,
            Brands_tags = Brands_tags,
            categories_tags = categories_tags,
            Categories_Tags = Categories_Tags,
            categories_en = categories_en,
            Categories_En = Categories_En,
            countries=countries,
            Countries = Countries,
            countries_tags = countries_tags,
            Countries_Tags = Countries_Tags,
            countries_en = countries_en,
            Countries_en = Countries_en,
            ingredients_text = ingredients_text,
            Ingredients_Text = Ingredients_Text,
            image_url = image_url,
            Image_url = Image_url,
            image_small_url = image_small_url,
            Image_Small_url = Image_Small_url,
            image_ingredients_url = image_ingredients_url,
            Image_Ingredients_url = Image_Ingredients_url,
            image_ingredients_small_url = image_ingredients_small_url,
            Image_Ingredients_Small_url = Image_Ingredients_Small_url,
            image_nutrition_url = image_nutrition_url,
            Image_Nutrition_url = Image_Nutrition_url,
            image_nutrition_small_url = image_nutrition_small_url,
            Image_Nutrition_Small_url = Image_Nutrition_Small_url,
            User_ID = User_ID,
            UserID = UserID,
            productID = productID,
            ProductID = ProductID)

        try:
            cur.execute(query)
        # To insert multiple rows into a table, use the executemany() method.
        # this except error is in the case if multiple columns are being attempted to be inserted into the database
        except:
            cur.executemany(query)

        db_connection.commit()
        cur.close()
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    finally:
        if db_connection:
            db_connection.close()

# return info for a wishlist entry at a time
# need both user ID and product ID for the specific entry
def _get_wish_list_individual(UserID, ProductID):
    try:
        db_name = "wish_list"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM wish_list 
         WHERE User_ID = '{}' AND productID = '{}' """.format(UserID, ProductID)

        cur.execute(query)

        result = (cur.fetchall())
        wish = _map_values(result)
        cur.close()
    except Exception:
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return wish

def _get_wish_list_all(UserID):
    try:
        db_name = "wish_list"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM wish_list 
         WHERE User_ID = '{}' """.format(UserID)

        cur.execute(query)

        result = (cur.fetchall())
        wishlist = _map_values(result)
        cur.close()
    except Exception:
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return wishlist


# if __name__ == "__main__":
#


  # the following code may become useful at some point
        # query = """
        #           UPDATE  wish_list
        #           SET
        #               `{User_ID}` = '{UserID}',
        #               `{User_Name}` = '{UserName}',
        #               `{productID}` = '{ProductID}',
        #               `{code}` = '{Code_Wish}',
        #               `{product_name}` = '{Product_name}',
        #               `{quantity}` = '{Quantity}',
        #               `{brands}` = '{Brands}',
        #               `{brands_tags}` = '{Brands_tags}',
        #               `{categories_tags}` = '{Categories_Tags}',
        #               `{categories_en}` = '{Categories_En}',
        #               `{countries}` = '{Countries}',
        #               `{countries_tags}` = '{Countries_Tags}',
        #               `{countries_en}` = '{Countries_en}',
        #               `{ingredients_text}` = '{Ingredients_Text}',
        #               `{image_url}` = '{Image_url}',
        #               `{image_small_url}` = '{Image_Small_url}',
        #               `{image_ingredients_url}` = '{Image_Ingredients_url}',
        #               `{image_ingredients_small_url}` = '{Image_Ingredients_Small_url}',
        #               `{image_nutrition_url}` = '{Image_Nutrition_url}',
        #               `{image_nutrition_small_url}` = '{Image_Nutrition_Small_url}'
        #           WHERE `{User_ID}` = '{UserID}' AND  `{productID}` = '{ProductID}'
        #           """.format(
        #     User_ID = User_ID,
        #     UserID = UserID,
        #     User_Name = User_Name,
        #     UserName = UserName,
        #     productID = productID,
        #     ProductID = ProductID,
        #     code = code,
        #     Code_Wish = Code_Wish,
        #     product_name = product_name,
        #     Product_name = Product_name,
        #     quantity = quantity,
        #     Quantity = Quantity,
        #     brands = brands,
        #     Brands = Brands,
        #     brands_tags = brands_tags,
        #     Brands_tags = Brands_tags,
        #     categories_tags = categories_tags,
        #     Categories_Tags = Categories_Tags,
        #     categories_en = categories_en,
        #     Categories_En = Categories_En,
        #     countries=countries,
        #     Countries = Countries,
        #     countries_tags = countries_tags,
        #     Countries_Tags = Countries_Tags,
        #     countries_en = countries_en,
        #     Countries_en = Countries_en,
        #     ingredients_text = ingredients_text,
        #     Ingredients_Text = Ingredients_Text,
        #     image_url = image_url,
        #     Image_url = Image_url,
        #     image_small_url = image_small_url,
        #     Image_Small_url = Image_Small_url,
        #     image_ingredients_url = image_ingredients_url,
        #     Image_Ingredients_url = Image_Ingredients_url,
        #     image_ingredients_small_url = image_ingredients_small_url,
        #     Image_Ingredients_Small_url = Image_Ingredients_Small_url,
        #     image_nutrition_url = image_nutrition_url,
        #     Image_Nutrition_url = Image_Nutrition_url,
        #     image_nutrition_small_url = image_nutrition_small_url,
        #     Image_Nutrition_Small_url = Image_Nutrition_Small_url,
        #     User_ID = User_ID,
        #     UserID = UserID,
        #     productID = productID,
        #     ProductID = ProductID
        # )