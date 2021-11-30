#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib as plt

# MY MODULE!
import ListDF as ldf
from ListDF import *

from sklearn.feature_extraction.text import TfidfVectorizer


url = 'https://world.openbeautyfacts.org/data/en.openbeautyfacts.org.products.csv'


# 18843 rows x 176 columns
f = pd.read_csv(url, sep='\t', low_memory=False)    # Download last version of the OBF CSV DB from URL
# f = pd.read_csv('en.openbeautyfacts.org.products.csv', sep='\t', low_memory=False)    # From file
# type(f)

# headers = list(f.columns)
# len(headers)                    # 176

"""
DB FIELDS
    productID INTEGER PRIMARY KEY,    # INDEX
	code MEDIUMTEXT NULL,
    product_name VARCHAR(500) NULL,
    quantity VARCHAR(100) NULL,
    brands VARCHAR(500) NULL,
    brands_tags VARCHAR(500) NULL,
    categories_tags VARCHAR(500) NULL,
    categories_en VARCHAR(500) NULL,
    countries VARCHAR(500) NULL,
    countries_tags VARCHAR(500) NULL,
    countries_en VARCHAR(500) NULL,
    ingredients_text VARCHAR(1000) NULL,
    image_url VARCHAR(1000) NULL,
    image_small_url VARCHAR(1000) NULL,
    image_ingredients_url VARCHAR(1000) NULL,
    image_ingredients_small_url VARCHAR(1000) NULL,
    image_nutrition_url VARCHAR(1000) NULL,
    image_nutrition_small_url VARCHAR(1000) NULL
"""
# 18843 rows x 7 columns
# subf = f[['code', 'product_name', 'brands', 'ingredients_text', 'categories', 'categories_tags', 'categories_en']]

#####################
# # TABLE Aa (18843 rows x 18 columns)
# Only keep the columns we are interested in
subf = f[['code',
        'product_name',
        'ingredients_text', # put here so we see it better
        'quantity',
        'brands',
        'brands_tags',
        'categories',   # added
        'categories_tags',
        'categories_en',
        'countries',
        'countries_tags',
        'countries_en',
        'image_url',
        'image_small_url',
        'image_ingredients_url',
        'image_ingredients_small_url',
        'image_nutrition_url',
        'image_nutrition_small_url']]

# Get rid of the NaN values and replace them with empty strings ''
subf = subf.fillna('')

#####################
# # TABLE Ab (7082 rows x 18 columns)
# FILTER for rows with ingredients and get rid of the empty ones  
subf = subf.loc[subf['ingredients_text'] != ''] 
# subf

# To avoid error message when using df_func
# AttributeError: 'float' object has no attribute 'split'
# subf = subf[subf['ingredients_text'].notnull()]
# subf

#####################
# # PROBLEM: Some lists of ingredients are not separated by commas! >.<
# subf['ingredients_text_list'][18842]
# # SOLUTION:
# Replace full stops, semicolons and bulletpoints into commas in the ingredients_text column

# DOESN'T WORK PRoPERLY: Cuts last letter of every word before a comma >.< 
# Function replace_by_commas() from my module ListDF!
# replace_by_commas(subf,'ingredients_text')

# subf['ingredients_text'] = subf['ingredients_text'].replace('.', ',')  # seems to cause trouble
subf['ingredients_text'] = subf['ingredients_text'].str.replace('∙', ',')
subf['ingredients_text'] = subf['ingredients_text'].str.replace(';', ',')
subf['ingredients_text'] = subf['ingredients_text'].str.lower()
# subf['ingredients_text']

# subf
#####################
## SAVE DF as CSV: TABLE Ab (subf) (7082 rows x 18 columns)
subf.to_csv(r'OBF_TABLE_Ab.csv',  header = True, index = True, index_label='productID')


# #####################
# # # TABLE Ac (7082 rows x 22 columns)
# # New columns with ingredients and categories as lists in lower case --> 18843 rows x 22 columns
# # Function df_func_string_to_list_strip_lower() from my module ListDF!
df_func_string_to_list_strip_lower(subf, 'ingredients_text')
df_func_string_to_list_strip_lower(subf, 'categories')
df_func_string_to_list_strip_lower(subf, 'categories_tags')
df_func_string_to_list_strip_lower(subf, 'categories_en')

# # # Reorganise the order of columns so each column_list is next to its original colum
subf = subf[['code',
		'product_name',
		'ingredients_text',
		'ingredients_text_list',
		'quantity',
		'brands',
		'brands_tags',
		'categories',
		'categories_list',
		'categories_tags',
		'categories_tags_list',
		'categories_en',
		'categories_en_list',
		'countries',
		'countries_tags',
		'countries_en',
		'image_url',
		'image_small_url',
		'image_ingredients_url',
		'image_ingredients_small_url',
		'image_nutrition_url',
		'image_nutrition_small_url']]

# subf

#####################
## SAVE DF as CSV: TABLE Ac (subf) (7082 rows x 22 columns)
subf.to_csv(r'OBF_TABLE_Ac.csv',  header = True, index = True, index_label='productID')


# ############################################################
# ### TABLE B: ORDERED INGREDIENTS FOR EACH PRODUCT BY INDEX
# # """
# # https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
# # """
# # Now we expand the True_List_Stuff lists in a new dataframe, while keeping the order of the elements:
# # TABLE B (7082 rows x 118 columns)
ingredients_table = subf["ingredients_text_list"].apply(pd.Series)

# ingredients_table

#####################
## SAVE DF as CSV: TABLE B (ingredients_table)
ingredients_table.to_csv(r'OBF_TABLE_B.csv',  header = True, index = True, index_label='productID')


# ############################################################
# #################### TO BE CONTINUED #######################
# ############################################################
# ############################################################
# ############################################################

### CHANGE NAME!!! 
# ingredients_text_list_expanded_v1 = ingredients_table 

# Get rid of the NaN values
# # ingredients_text_list_expanded_v1 = ingredients_text_list_expanded_v1.fillna('')
# ingredients_text_list_expanded_v1

# # Now let's count which values are nº1 in the lists more frequently  --> aqua/water/eau
# ingredients_text_list_expanded_v1.iloc[:,0].value_counts(normalize = True)

# # Now let's count which values are nº2 in the lists more frequently
# # sodium laureth sulfate / glycerin / aqua / cetearyl alcohol  
# ingredients_text_list_expanded_v1.iloc[:,1].value_counts(normalize = True)

# # Now let's count which values are nº3 in the lists more frequently
# # glycerin / cocamidopropyl betaine / sodium chloride / hydrated silica 
# ingredients_text_list_expanded_v1.iloc[:,2].value_counts(normalize = True)


############################################################

# # Target single ingredients and find out how many times they were named at each position of the lists:

# def get_rankings(item, df):
    
#     # Empty dict for results
#     item_count_dict = {}
    
#     # For every tag in df
#     for i in range(df.shape[1]):
        
#         # Calculate % of cases that tagged the item
#         val_counts = df.iloc[:,i].value_counts(normalize = True)
#         if item in val_counts.index:
#             item_counts = val_counts[item]
#         else:
#             item_counts = 0
        
#         # Add score to dict
#         item_count_dict["tag_{}".format(i)] = item_counts
    
#     return item_count_dict

# # get_rankings(item = "glyceryl stearate", df = ingredients_text_list_expanded_v1)
# get_rankings(item = "glycerin", df = ingredients_text_list_expanded_v1)


############################################################
### Filter the dataframe depending on the value of a column

# # Subset based on specific value of the first ingredient (index 0)
# # Glycerin as a 1st ingredient: 36 rows
# filter_ingredients_text_list_expanded_v1_glycerin_1 = ingredients_text_list_expanded_v1.loc[ingredients_text_list_expanded_v1[0] == 'glycerin'] 
# filter_ingredients_text_list_expanded_v1_glycerin_1

# # Subset based on specific value of the second ingredient (index 1)
# # Glyceryl Stearate as a 2nd ingredient: 6 rows
# filter_ingredients_text_list_expanded_v1_glyceryl_stearate_2 = ingredients_text_list_expanded_v1.loc[ingredients_text_list_expanded_v1[1] == 'glyceryl stearate'] 
# filter_ingredients_text_list_expanded_v1_glyceryl_stearate_2

# Subset based on specific value of the third ingredient (index 2)
# Cetrimonium Chloride as a 3rd ingredient: 6 rows    (not Stearaikonium Chloride)
# filter_ingredients_text_list_expanded_v1_cetrimonium_chloride_3 = ingredients_text_list_expanded_v1.loc[ingredients_text_list_expanded_v1[2] == 'cetrimonium chloride'] 
# filter_ingredients_text_list_expanded_v1_cetrimonium_chloride_3

# # Subset based on specific value of the third ingredient (index 2)
# # Stearyl Alcohol as a 3rd ingredient: 14 rows
# filter_ingredients_text_list_expanded_v1_stearyl_alcohol_3 = ingredients_text_list_expanded_v1.loc[ingredients_text_list_expanded_v1[2] == 'stearyl alcohol'] 
# # filter_ingredients_text_list_expanded_v1_stearyl_alcohol_3

# # Subset based on specific value of the third ingredient (index 2)
# # Stearalkonium Chloride as a 3rd ingredient: 3 rows    (not Stearaikonium Chloride)
# filter_ingredients_text_list_expanded_v1_stearalkonium_chloride_3 = ingredients_text_list_expanded_v1.loc[ingredients_text_list_expanded_v1[2] == 'stearalkonium chloride'] 
# filter_ingredients_text_list_expanded_v1_stearalkonium_chloride_3

# Other conditioner molecules
# Behentrimonium methosulfate
# Cetrimonium bromide


### FILTER TABLE A
#filtered_subf = subf.loc[subf['column_name'] == some_value]

# Select rows by index
#subdf.loc[ index , : ]

# for multiple rows
# indices_glycerin_1 = filter_ingredients_text_list_expanded_v1_glycerin_1.index.values.tolist()
# indices_glycerin_1    # indices of products having glycerin as 1st ingredient
# filtered_subf_glycerin_1 = subf.loc[indices_glycerin_1, :]
# len(filtered_subf_glycerin_1)    # 36 products
