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
    return cnx

# lord only know if i even need this function , as i have later updated the MySQL database with a seperate function
# im following lesson 20 and im a bit confused
def _map_values(result):
    mapped = []
    for item in result:
        mapped.append(
            {
                "productID": item[0],
                "code": item[1],
                "product_name": item[3],
                "quantity": item[4]
                "brands": item[5],
                "brands_tags": item[6],
                "categories_tags": item[7],
                "categories_en": item[8],
                "countries": item[9],
                "countries_tags": item[10],
                "countries_en": item[11],
                "ingredients_text": item[12],
                "image_url": item[13],
                "image_small_url": item[14],
                "image_ingredients_url": item[15],
                "image_ingredients_small_url": item[16],
                "image_nutrition_url": item[17],
                "image_nutrition_small_url": item[18],
            }
        )
    return mapped

# have no idea if this code even works or makes sense as I don't have everyones codes so i don't actually
# know how the DB will be fetching the data and inserting it

def add_wish_list(UserID, ProductID, Code_Wish, Product_name, Quantity,
    Brands, Brands_tags, Categories_Tags, Countries_en, Ingredients_Text, Image_url, Image_Small_url, Image_Ingredients_url,
    Image_Ingredients_Small_url, Image_Nutrition_url, Image_Nutrition_Small_url):
    try:
        db_name = "wish_list"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
                  UPDATE  wish_list
                  SET 
                      `{productID}` = '{ProductID}',
                      `{code}` = '{Code_Wish}',
                      `{product_name}` = '{Product_name}',
                      `{quantity}` = '{Quantity}',
                      `{brands}` = '{Brands}',
                      `{brands_tags}` = '{Brands_tags}',
                      `{categories_tags}` = '{Categories_Tags}',
                      `{categories_en}` = '{Categories_En}',
                      `{countries}` = '{Countries}',
                      `{countries_tags}` = '{Countries_Tags}',
                      `{countries_en}` = '{Countries_en}',
                      `{ingredients_text}` = '{Ingredients_Text}',
                      `{image_url}` = '{Image_url}',
                      `{image_small_url}` = '{Image_Small_url}',
                      `{image_ingredients_url}` = '{Image_Ingredients_url}',
                      `{image_ingredients_small_url}` = '{Image_Ingredients_Small_url}', 
                      `{image_nutrition_url}` = '{Image_Nutrition_url}', 
                      `{image_nutrition_small_url}` = '{Image_Nutrition_Small_url}'
                  WHERE `{User_ID}` = '{UserID}' AND  `{productID}` = '{ProductID}'
                  """.format(
            productID = ProductID,
            code = Code_Wish,
            product_name = Product_name,
            quantity = Quantity,
            brands = Brands,
            brands_tags = Brands_tags,
            categories_tags = Categories_Tags,
            categories_en = Categories_En,
            countries = Countries,
            countries_tags = Countries_Tags,
            countries_en = Countries_en,
            ingredients_text = Ingredients_Text,
            image_url = Image_url,
            image_small_url = Image_Small_url,
            image_ingredients_url = Image_Ingredients_url,
            image_ingredients_small_url = Image_Ingredients_Small_url,
            image_nutrition_url = Image_Nutrition_url,
            image_nutrition_small_url = Image_Nutrition_Small_url,
            User_ID = UserID
        )

        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    finally:
        if db_connection:
            db_connection.close()

# return info for a wishlist entry at a time
# need both user ID and product ID for the specific entry
def _get_wish_list(UserID, ProductID):
    try:
        db_name = "wish_list"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM wish_list 
         WHERE User_ID = '{}' AND productID = '{}' """.format(UserID, ProductID)

        cur.execute(query)

        result = (cur.fetchall())
        wish = _get_wish_list(result)
        cur.close()
    except Exception:
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return wish


# if __name__ == "__main__":
#

