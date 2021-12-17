import mysql.connector
from config import USER, PASSWORD, HOST
from pprint import pp 


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


def _map_values(result):
    mapped = []
    for item in result:
        mapped.append(
            {
               "productID": item[0],
                "code": item[1],
                "product_name": item[2],
                "ingredients_list": item[11],
                "brands": item[4], 
                "quantity": item[3], 
                "brands_tags": item[5], 
                "categories": item[7],
                "categories_tags": item[6], 
                "categories_en": item[7], 
                "countries": item [8],
                "countries_tags": item [9],
                "countries_en": item[10], 
                "image_url": item[12], 
                "image_small_url": item[13], 
                "image_ingredients_url": item[14], 
                "image_ingredients_small_url": item[15], 
                "image_nutrition_url": item[16], 
                "image_nutrition_small_url": item[17], 
            }
        )
    return mapped


#I included this functon to reduce the repetition of the try, except and finall blocks in other functions 
# Having these within its own function will also make testing easier and I believe the code would be more readable 
def exception_handler(query,error_message): 
    """This function is the exception handler for exceptions that may arise when connecting to the 
    db """
    try:
        db_name = 'wish_list' #i am still not sure what the correct database name is meant to be here 
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        cur.execute(query) 
        db_connection.commit()
        cur.close()

    except Exception:
        raise DbConnectionError(error_message) 
    #you pass whatever error message depending on the function that exception_handler is called within 
    #eg of error messages could be "failure to insert data" , "failure to delete data"

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )
    return 





def add_to_wishlist(user_id,user_name,wishlist_dict):
    """This function receives a wishlist item in the form of a dict and inserts it into the database """
    columns_string = "(User_ID, User_Name"
    values_string = "({user_id},'{user_name}' ".format(
        user_id=user_id, 
        user_name=user_name
        ) #userId is an int 


    for key,value in wishlist_dict.items():

        columns_string += ", {key} ".format(key=key)
        
        if isinstance(value, int):
            values_string += ", {value}".format(value=value) #productid is an int 
        else:
            values_string += ", '{value}' ".format(value=value) #all other values are strings 

    columns_string += ")"
    values_string += ")"

    query = """
            INSERT INTO wish_list
            {tuple_of_column_names}
            VALUES
            {tuple_of_values}
            """.format(
                tuple_of_column_names = columns_string,
                tuple_of_values = values_string

            )
    print(query) #remove after testing 

    error_message = "Failure to insert data into DB"

    exception_handler(query,error_message) #returns the return statement 
    display_statement = "Wishist item added for user {user_name} with user ID {user_id}".format(
        user_name=user_name,
        user_id = user_id
        )
    
    print(display_statement)
    
    

    




def remove_from_wishlist():
    pass









#Printing the query string of the add_to_wishlist() function to make sure it's what I want 
"""
wishlist_dict = {
    "productID ": 6,
	"code": '62263436',
    "product_name": 'Huile de massage à l\'arnica',
    "quantity": '100 ml',
    "brands": 'Weleda',
    "brands_tags": 'weleda',
    "categories_tags": 'en:body,en:body-oils,fr:huile-de-massage',
    "categories_en": 'Body,Body-oils,fr:huile-de-massage',
    "countries": 'France',
    "countries_tags": 'en:france',
    "countries_en": 'France',
    "ingredients_text": 'helianthus annuus (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles',
    "image_url": 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg',
    "image_small_url": 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg',
    "image_ingredients_url": '',
    "image_ingredients_small_url": '',
    "image_nutrition_url": '',
    "image_nutrition_small_url": ''
}


add_to_wishlist(1,"Chizu",wishlist_dict)


Result when i print the query from the add_to_wishlist() function :


 INSERT INTO wish_list
            (User_ID, User_Name, productID  , code , product_name , quantity , brands , brands_tags , categories_tags , categories_en , 
            countries , countries_tags , countries_en , ingredients_text , image_url , image_small_url , image_ingredients_url , image_ingredients_small_url , 
            image_nutrition_url , image_nutrition_small_url )
            VALUES
            (1,'Chizu' , 6 , '62263436' , 'Huile de massage à l'arnica' , '100 ml' , 'Weleda' , 'weleda' , 'en:body,en:body-oils,fr:huile-de-massage' , 
            'Body,Body-oils,fr:huile-de-massage' , 'France' , 'en:france' , 'France' , 'helianthus annuus (sunflower) seed oil, olea europaea (olive) fruit oil, 
            fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles' , 
            'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg' , 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg' , 
            '' , '' , '' , '' )
"""



