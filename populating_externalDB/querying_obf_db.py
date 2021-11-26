import mysql.connector

from config import USER, HOST, PASSWORD 
from pprint import pp 
#in future modifications, maybe add error handling as a decorator to reduce  repetitive code. 
# still need to host database in cloud but data retrieval functions seem to be working fine
# can decorate the funtions with API routing when working with flask. like we did in the lessons 

def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=db_name,
    )
    return cnx #returns context 

class DbConnectionError(Exception): #inherits exception class so has all its abilities 
    pass

def fetch_product_ids(ingredient): 
    """this function gets a list of productID's corresponding to a certain ingredient"""
    try:
        db_name = "external_obf_testing"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print("Connected to DB %s" % db_name)

        ########################################
        query = """
                    SELECT productID FROM ID_ingredients 
                    WHERE ingredients_text LIKE "{}"

                """.format(ingredient)
                # have to consider using the % and _ operators to catch ingredients that arent exact 
                # but still pretty close, something like: WHERE ingredients_text LIKE "%water%"

        #print(query)
        cursor.execute(query) 
        id_list = []
        for row in cursor:
            id_list.append(row[0])
        #########################################
        

        
        db_connection.commit()
        cursor.close()

    except Exception:
        raise DbConnectionError("Fails to insert data into DB")

    finally:
        
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return id_list 



def fetch_products(ingredient,query):
    """This function takes a list of productID's and fetches the corresponding 
    product info of each, it then makes a dictionary list with all the information 
    It accepts a query parameter which allows for flexibility when searching for products 
    that contain or do not contain a certain ingredient 
    """
    
    productid_list = fetch_product_ids(ingredient)
    #print(productid_list) #just for testing 

    try:
        db_name = "external_obf_testing"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print("Connected to DB %s" % db_name)

        ########################################
        query += "{}".format(tuple(productid_list))

        #print(query)
        cursor.execute(query) 
        result = cursor.fetchall() #list of records 
        
        #########################################
        
        
        db_connection.commit()
        cursor.close()

    except Exception:
        raise DbConnectionError("Fails to insert data into DB")

    finally:
        
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    
    return result #format properlly later. should be a list of dictionaries with appropriate keys 


ingredient = "water"
# query = """ SELECT * FROM products WHERE productID IN """
query = """ SELECT product_name FROM products WHERE productID IN """
pp(fetch_products(ingredient,query))


## should work if you also want all products that don't contain water 
# within fetch_products() you get all the productID's corresponding to the ingredient water
# then, this time,  your query should be NOT IN instead of IN :

not_ingredient = "water"
query = """ SELECT product_name FROM products WHERE productID NOT IN """
pp(fetch_products(ingredient,query))