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


# if __name__ == "__main__":
#