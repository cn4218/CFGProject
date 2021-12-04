dict_ = {   
    'filter': 'ordered', 
    'data': {'1': ['water', True],
             '2': ['glycerin ', False], 
             '3': ['alcohol', True], 
             '4': ['parfum', True], 
             '5': ['', True]
            }
        }
    



def format_input(ingredient_input): 
    #need to make sure white spaces are removed before they are sent over the api 
    """ This takes a dictionary input in the structure 
    {"1":["ingredient1",True], "2": ["ingredient2",False],.....,"5":["ingredient5",True]}
    and creates a dictionary of 2 list values containing ingredients to include and not to include 
    """
    ingredient_list = []
    not_ingredient_list = []
    for key,value in ingredient_input.items():
        ingredient,decision = value
        #if decision = True it means include ingredient, otherwise don't include 
        if ingredient: #if not empty string 
            if decision: 
                tup = (key,ingredient)
                ingredient_list.append(tup)  
            else: 
                
                not_ingredient_list.append(ingredient) 
    return {"included": ingredient_list, "not_included": not_ingredient_list}


print(dict_)
print(format_input(dict_["data"]))
