#!/usr/bin/env python3



"""
This is a small module with functions to be used on dataframes and lists values
(Claire BOITET)
"""


import numpy as np
import pandas as pd

def strip_list(l: list) -> list:
    """Strips unnecessary initial and final spaces in elements of a list"""
    # List comprehension to strip useless spaces
    _list = [x.strip(' ') for x in _list]
    return _list

def string_to_list_strip(string: str) -> list:
    """Turns a string into a list and strips its elements trailing spaces"""
    # Takes the content of the 'Stuff' columns and transforms it into a list
    _list = list(map(str, string.split(",")))
    # List comprehension to strip useless spaces
    _list = [x.strip(' ') for x in _list]
    return _list

def string_to_list_strip_lower(string: str) -> list:
    """Turns a string into a list and strips its elements trailing spaces --> strl2"""
    # Takes the content of the 'Stuff' columns and transforms it into a list
    _list = list(map(str, string.split(",")))
    # List comprehension to strip useless spaces
    _list = [x.strip(' ') for x in _list]
    _list = [x.lower() for x in _list]
    return _list


def df_func(df, col:str, new_col:str, function):
    """Creates a new pandas dataframe column by applying a function to another column"""
    df[new_col] = df[col].apply(function)
    return df[new_col]


def df_func_string_to_list_strip_lower(df,column:str):
    """Creates new columns as lists in lower case"""
    column_list = column + '_list'
    df_func(df, column, column_list, string_to_list_strip_lower)


def replace_by_commas(df,column:str):
    """
    WORKS! Or does it?
    Replaces full stops, semicolons and bulletpoints into commas in a given dataframe column
    """
    # # This syntax doesn't work for some reason...
    # df[column] = df[column].replace({' , ':',',', ':',',' ,':',',' . ':',','. ':',',' .':',','.':',',' ∙ ':',',' ∙':',','∙ ':',','∙':','}) 
    # df[column] = df[column].str.replace(' , ',',') # seem to cause trouble?
    # df[column] = df[column].str.replace(', ',',')
    # df[column] = df[column].str.replace(' ,',',')
    # df[column] = df[column].str.replace(' . ',',')
    # df[column] = df[column].str.replace('. ',',')
    # df[column] = df[column].str.replace(' .',',')
    df[column] = df[column].str.replace('.', ', ')
    # df[column] = df[column].str.replace(' ∙ ',',')   
    # df[column] = df[column].str.replace(' ∙',',')
    # df[column] = df[column].str.replace('∙ ',',')
    df[column] = df[column].str.replace('∙', ', ')
    df[column] = df[column].str.replace(';', ', ')


# #*************************************************

def normalize_space(s):
    """From John Machin - Return string stripped of leading/trailing whitespace
    and with internal runs of whitespace replaced by a single SPACE"""
    # This should be a str method :-(
    return ' '.join(s.split())



def boolean_df(item_lists, unique_items):
    """From Max Hildorf — Create a dataframe where rows stay the same as before, but where 
    every element of the list element is assigned its own column with a boolean in it"""
# Create empty dict
    bool_dict = {}
    
    # Loop through all the list items
    for i, item in enumerate(unique_items):
        
        # Apply boolean mask
        bool_dict[item] = item_lists.apply(lambda x: item in x)
            
    # Return the results as a dataframe
    return pd.DataFrame(bool_dict)



def to_1D(series):
    """From Max Hildorf — Creates a new dataframe by concatenating all of the elements 
    of another dataframe then giving each o"""
    return pd.Series([x for _list in series for x in _list])