import mysql.connector 
from config import USER, HOST, PASSWORD 
import requests 
from pprint import pp 

"""
- This script makes a connection to the external_obf_testing database 

- It then uses the get_ingredients function to send a request to the experiemental OBF api to fetch 
all its ingredients and put then in a list 

- The final function makes a query to the database where it inserts contents of the list & corresponding index 
into the ingredients table of the database.

"""

def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=db_name,
    )
    return cnx #returns context 

# I noticed that i run into errors when i try to insert a string with a colon into the DB. 
# for example fr:parfum 
# So i am going to use the str.replace(old_chr, new_chr) function to replace ":"  with spaces " "



#for some reason I only get 9999 ingredients & found out there were some duplicate entries so its even less 
# than that 
def get_ingredients():
    url = 'https://world.openbeautyfacts.org/ingredients.json'
    response = requests.get(url)
    dict_ = response.json()
    # pp(dict_)
    tag_list = dict_['tags']
    # print(len(tag_list)) #I am only seeing 10K ingredients 
    # pp(dict_['tags'])
    ingredients_list = []
    for idx in range(len(tag_list)):
        ig_dict = tag_list[idx]
        ingredient = ig_dict['name']
        # if ":" in ingredient:
        #     ingredient = ingredient.replace(":", " ")
        
        ingredients_list.append(ingredient)
    #pp(ingredients_list)
    ingredients_list = list(set(ingredients_list)) #check that i fully understand this 
    return ingredients_list


#get_ingredients()

class DbConnectionError(Exception): #inherits exception class so has all its abilities 
    pass

#error handling can be put into its own function and accept functions as arguments
#  #look into how to do this if it's even possible. It will help make code more concise

def insert_ingredients(): 
    try:
        db_name = "external_obf_testing"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print("Connected to DB %s" % db_name)

        query = """
            INSERT INTO ingredients 
            (IngredientID,Ingredient) 
            VALUES  """
        _string = ""
        ingredients = get_ingredients()
        length = len(ingredients)
        for idx in range(length):
            if idx != length-1: 
                _string += '({},"{}" ), \n'.format(idx,ingredients[idx])
            else:
                _string += '({},"{}" );'.format(idx,ingredients[idx])
        query += _string
        print(query)
        cursor.execute(query) 
        db_connection.commit()
        cursor.close()

    except Exception:
        raise DbConnectionError("Fails to insert data into DB")

    finally:
        
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# insert_ingredients()

#order of the day 

# extract ingredients from products table 
# try and split each string into a list with separator being a comma 
# join all lists together as you go along 
#find a way to create a dictionary lists of productID and corresponding ingredient 
# push that list to a new table 
import csv
def extract_ingredients():
    try:
        db_name = "external_obf_testing"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print("Connected to DB %s" % db_name)

        # query = """
        #     SELECT ingredients_text FROM products 
        #     """
        
        
        # cursor.execute(query) 
        # result = cursor.fetchall()
        
        # # print(type((result[0])))
        # # print((result[0]))
        # # stuff = ('',) # type string 
        # # print(type(stuff[0]))


        # # pp(result)
        # all_ingredients = []
        # for element in result:
        #     tup_string = element[0] #gives you the string in each tuple 
        #     temp_list = tup_string.split(",")
        #     all_ingredients.extend(temp_list)

        # pp(all_ingredients) 
        # # so we were able to successfully split by comma, the problem is that not all were separated by comma's
        # # the solution to this is just use the LIKE conditional in MySQL and the _ % operators to search when 
        # # someone asks us to search for an ingredient 
        # there is also a concern that this list might contain duplicates. Try and resolve later 

        #previously I tested to see if I could successfully split the ingredients, 
        # now I am going to get the productId as well and build a record list of productID and single ingredient 

        query = """
             SELECT productID, ingredients_text FROM products 
             """
        
        
        cursor.execute(query) 
        next = cursor.fetchone()
        all_ingredients = []
        while next is not None:
            productID, tup_string = next  #deconstruct tuple 
            temp_list = tup_string.split(",") #split the string into a list of comma separated ingredients 
            
            #now we create our own tuple list in the format [(Id,ingredient1), (Id,ingredient2), ....]
            for element in temp_list:
                # if "\\" in element:
                #     element = element.replace("\\", "|")
                new_tuple = (productID,element)
                all_ingredients.append(new_tuple)
            next = cursor.fetchone()

       # pp(all_ingredients) #this works, moving on 
        # print(type(result))

    #     query = """
        
    #             INSERT IGNORE INTO ID_ingredients
    #             (productID,ingredients_text) 
    #             VALUES  
    #             """
    #     str_ = "" #using it to construct our values we want to insert. before we add it to the query

    #     for el in all_ingredients:
    #         id_ , ingredient = el 
    #         # if all_ingredients.index(el) != length-1: 
    #         str_ += '({},"{}" ), \n'.format(id_,ingredient)
    #         # else:
    #         #     str_ += '({},"{}" );'.format(id_,ingredient)
    #     query += str_
    #    # print(query)

    #     cursor.execute(query)
        db_connection.commit()
        cursor.close()



    except Exception:
        raise DbConnectionError("Fails to insert data into DB")

    finally:
        
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
        

# note: If you use 'b' for the mode, you will get a TypeError
# under Python3. You can just use 'w' for Python 3



    with open('ID_ingredients.csv','w') as f_obj:
        csv_=csv.writer(f_obj)
        csv_.writerow(['productID','ingredients_text'])
        for element in all_ingredients:
            csv_.writerow(element)

extract_ingredients()