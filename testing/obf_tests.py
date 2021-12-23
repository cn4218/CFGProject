from unittest.mock import patch
from unittest import TestCase, main
import pandas as pd
from operator import *
import mysql.connector

from obf_main import MockProductFrontEnd, run                                           

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent)) 
from CFGProject.scripts.obf_db_utils import _get_all_product_ids, get_productids_containing, get_products_by_ids, fetch_results, verify_product_id
from CFGProject.scripts.config import USER,PASSWORD,HOST

"""
File contains:
TestProductFrontEnd:
    test_unordered_containing_water(self,mock_inputs)
    test_unordered_containing_glycerin(self,mock_inputs)
    test_unordered_containing_parfum(self, mock_inputs)
    test_unordered_bicarb(self,mock_inputs)
    test_ordered_bicarb(self, mock_inputs)
    test_ordered_aqua(self, mock_inputs)
    test_ordered_water(self, mock_inputs)
    test_bad_input(self,mock_inputs)
    test_bad_input_result(self,mock_inputs)
    test_allergic_to_ingredients_aqua(self,mock_inputs)
    test_allergic_to_ingredients(self,mock_inputs)
    test_no_water(self, mock_inputs)
    test_null_values_order(self,mock_inputs)
    test_result_save(self,mock_inputs)

TestAPIRecall:
    test_a_recall(self, mock_inputs)
    test_null_values_a(self,mock_inputs)

TestDBUtils:
    test_empty_input_list(self)
    test_one_search_id(self)
    test_verify(self)
    test_verify_correct_id(self)

"""

class TestProductFrontEnd(TestCase):
    def setUp(self):
        self.mock = MockProductFrontEnd()

    @patch('builtins.input',side_effect=['n','water','y','glycerin','n','','','','','','',''])
    def test_unordered_containing_water(self,mock_inputs):
        """
        Mock inputs for unordered search containing water and not containing glycerin.
        Test function firstly converts dictionary output to a dataframe and then checks if the string water is contained in every result in ingredients_text column.
        Then checks if the string glycerin appears zero times.
        """
        output,_ = run()
        df = pd.DataFrame(output)
        self.containg_water = df['ingredients_text'].str.contains('water').sum()
        self.conatining_glycerin = df['ingredients_text'].str.contains('glycerin').sum()
        self.assertEqual(len(df),self.containg_water)
        self.assertEqual(0,self.conatining_glycerin)

    @patch('builtins.input',side_effect=['n','water','n','glycerin','y','citric acid','y','','','','',''])
    def test_unordered_containing_glycerin(self,mock_inputs):
        """
        Mock inputs for unordered search not containing water but containing glycerin and citric acid.
        Test function firstly converts dictionary output to a dataframe and then checks if the strings glycerin and citric acide are in every result in ingredients_text column.
        Then checks if the string water appears zero times.
        """

        output,_ = run()
        df = pd.DataFrame(output)
        containg_water = df['ingredients_text'].str.contains('water').sum()
        conatining_glycerin = df['ingredients_text'].str.contains('glycerin').sum()
        conatining_citric_acid = df['ingredients_text'].str.contains('citric acid').sum()
        self.assertEqual(len(df),conatining_glycerin)
        self.assertEqual(0,containg_water)
        self.assertEqual(len(df),conatining_citric_acid)

    @patch('builtins.input',side_effect=['n','bicarbonate de sodium','n','parfum','y','limonene','y','','','','',''])
    def test_unordered_containing_parfum(self, mock_inputs):
        """
        Mock inputs for unordered search not containing bicarbonate de sodium but containing parfum and limonene.
        Test function firstly converts dictionary output to a dataframe and then checks if the strings parfum and limonene or límonene are in every result in ingredients_text column.
        Then checks if the string bicarbonate de sodium appears zero times.
        """
        output,_ = run()
        df = pd.DataFrame(output)
        df['ingredients_text'] = df['ingredients_text'].replace('í','i')
        containg_bicarb = df['ingredients_text'].str.contains('bicarbonate de sodium').sum()
        containing_parfum = df['ingredients_text'].str.contains('parfum').sum()
        containing_limonene = df['ingredients_text'].str.contains('limonene|límonene').sum()

        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containing_parfum)
        self.assertEqual(len(df),containing_limonene)
        
    @patch('builtins.input',side_effect=['n','bicarbonate de sodium','n','geraniol','y','hexyl cinnamal','y','alcohol','n','water','n',''])
    def test_unordered_bicarb(self,mock_inputs):
        """
        Mock inputs for unordered search not containing bicarbonate de sodium, alcohol and water but containing geraniol and hexyl cinnamal.
        Test function firstly converts dictionary output to a dataframe and then checks if the strings geraniol, hexyl cinnamal are in every result in ingredients_text column.
        Then checks if the string bicarbonate de sodium,alcohol and water appears zero times.
        """

        output,_ = run()
        df = pd.DataFrame(output)
        containg_bicarb = df['ingredients_text'].str.contains('bicarbonate de sodium').sum()
        containing_geraniol = df['ingredients_text'].str.contains('geraniol').sum()
        containing_hexyl = df['ingredients_text'].str.contains('hexyl cinnamal').sum()
        containing_alcohol = df['ingredients_text'].str.contains('alcohol').sum() 
        containing_water = df['ingredients_text'].str.contains('water').sum()  
        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containing_geraniol)
        self.assertEqual(len(df),containing_hexyl)
        self.assertEqual(0,containing_alcohol)
        self.assertEqual(0,containing_water)

    @patch('builtins.input',side_effect=['y','bicarbonate de sodium','n','aqua','y','','','alcohol','y','','',''])
    def test_ordered_bicarb(self, mock_inputs):
        """
        Mock inputs for ordered search not containing bicarbonate de sodium but aqua at 2nd position and alcohol at 4th position.
        Test function firstly converts dictionary output to a dataframe and then checks if the string aqua is in every result in 2nd position of list in ingredients_text column,
        and then if string alcohol is in every result in 4th position of list in ingredients_text column
        Then checks if the string bicarbonate de sodium appears zero times.
        """

        output,_ = run()
        df = pd.DataFrame(output)
        df['2nd ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[1])
        df['4th ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[3])
        containg_bicarb = df['ingredients_text'].str.contains('bicarbonate de sodium').sum()
        containg_aqua = df['2nd ingredient'].str.contains('aqua').sum()
        containing_alcohol = df['4th ingredient'].str.contains('alcohol').sum()
        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containg_aqua)
        self.assertEqual(len(df),containing_alcohol)

    @patch('builtins.input',side_effect=['y','aqua','y','isobutane','y','','','','','sodium tallowate','n',''])
    def test_ordered_aqua(self, mock_inputs):
        """
        Mock inputs for ordered search not containing sodium tallowate but aqua at 1st position and isobutane at 2nd position.
        Test function firstly converts dictionary output to a dataframe and then checks if the string aqua is in every result in 1st position of list in ingredients_text column,
        and then if string isobutane is in every result in 2nd position of list in ingredients_text column
        Then checks if the string sodium tallowate appears zero times.
        """

        output,_ = run()
        df = pd.DataFrame(output)
        df['1st ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[0])
        df['2nd ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[1])
        containg_aqua = df['1st ingredient'].str.contains('aqua').sum()
        containg_isobutane = df['2nd ingredient'].str.contains('isobutane').sum()
        containing_sod_tal = df['ingredients_text'].str.contains('sodium tallowate').sum()
        self.assertEqual(len(df),containg_aqua)
        self.assertEqual(len(df),containg_isobutane)
        self.assertEqual(0,containing_sod_tal)

    @patch('builtins.input',side_effect=['y','water','y','parfum','y','','','','','','',''])
    def test_ordered_water(self, mock_inputs):
        """
        Mock inputs for ordered search containing water at 1st position and parfum at 2nd position.
        Test function firstly converts dictionary output to a dataframe and then checks if the string water is in every result in 1st position of list in ingredients_text column,
        and then if string parfum is in every result in 2nd position of list in ingredients_text column
        """
        output,_ = run()
        df = pd.DataFrame(output)
        df['1st ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[0])
        df['2nd ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[1])
        containg_water = df['1st ingredient'].str.contains('water').sum()
        containg_parfum = df['2nd ingredient'].str.contains('parfum').sum()
        self.assertEqual(len(df),containg_water)
        self.assertEqual(len(df),containg_parfum)

    @patch('builtins.input',side_effect = ['y','water','y','water','n','','','','','','',''])
    def test_bad_input(self,mock_inputs):
        """
        Mock inputs for ordered search containing water at 1st position and not containing water.
        Checks if query returns no search results, and that a string is returned saying this.
        """
        output,_ = run()
        self.assertEqual('Query returns no search results',output)


    @patch('builtins.input',side_effect = ['y','water','y','Stearalkonium chloride','y','stearyl alcohol','y','butyrospermum parkii (beurre de karité)','n','caprylic/capric triglyceride','n',''])
    def test_bad_input_result(self,mock_inputs):
        """
        Mock inputs for ordered search containing ingredients in a order that no product has.
        Checks if query returns no search results, and that a string is returned saying this.
        """
        output,_ = run()
        self.assertEqual('Query returns no search results',output)


    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','',''])
    def test_allergic_to_ingredients_aqua(self,mock_inputs):
        """
        Mock inputs for unordered search not containing aqua, sodium, magnesium and amyl cinnamal.
        Test function firstly converts dictionary output to a dataframe and then checks if the strings aqua, magnesium, sodium and amyl cinnamal are not in any of the ingredients text column.
        """
        output,_ = run()
        df = pd.DataFrame(output)
        containing_water = df['ingredients_text'].str.contains('aqua').sum()
        containg_gycerin = df['ingredients_text'].str.contains('sodium').sum()
        containing_sodium = df['ingredients_text'].str.contains('magnesiume').sum()
        containing_hexyl = df['ingredients_text'].str.contains('amyl cinnamal').sum()
        self.assertEqual(0,containing_water)
        self.assertEqual(0,containg_gycerin)
        self.assertEqual(0,containing_sodium)
        self.assertEqual(0,containing_hexyl)

    @patch('builtins.input',side_effect = ['y','water','n','glycerin','n','sodium palmate','n','parfum','n','','',''])
    def test_allergic_to_ingredients(self,mock_inputs):
        """
        Mock inputs for unordered search not containing water, glycerin, sodium palmate and parfum.
        Test function firstly converts dictionary output to a dataframe and then checks if the strings water, glycerin, sodium palmate and parfum are not in any of the ingredients text column.
        """
        output,_ = run()
        df = pd.DataFrame(output)
        containing_water = df['ingredients_text'].str.contains('water').sum()
        containg_gycerin = df['ingredients_text'].str.contains('glycerin').sum()
        containing_sodium = df['ingredients_text'].str.contains('sodium palmate').sum()
        containing_hexyl = df['ingredients_text'].str.contains('parfum').sum()
        self.assertEqual(0,containing_water)
        self.assertEqual(0,containg_gycerin)
        self.assertEqual(0,containing_sodium)
        self.assertEqual(0,containing_hexyl)
    
    @patch('builtins.input',side_effect = ['n','water','n','','','','','','','','',''])
    def test_no_water(self, mock_inputs):
        """
        Mock inputs for unordered search not containing water.
        Test function firstly converts dictionary output to a dataframe and then checks if the string water is not in any of the ingredients text column.
        Then checks the length of the entire products list containing water subtracted from the entire products list to make sure the length is equal to the length of the result.
        """
        output,_ = run()
        df = pd.DataFrame(output)
        containing_water = df['ingredients_text'].str.contains('water').sum()
        result_all = _get_all_product_ids()
        result_water = get_productids_containing('water')
        expected_length = len(result_all)-len(result_water)
        self.assertEqual(0,containing_water)
        self.assertEqual(len(df),expected_length)

    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','',''])
    def test_null_values_order(self,mock_inputs):
        """
        Mock inputs to test if there are fewer occurances of string NotAvailable at top of products list and that the number of occurances increases as the list goes on.
        Testing the effectiveness of display_less_null_values function in obf_db_utils.
        """
        output,_ = run()
        occurence_na = []
        for item in output:
            count_occ = countOf(item.values(), 'NotAvailable')
            occurence_na.append(count_occ)      
        self.assertEqual(occurence_na,sorted(occurence_na))


    @patch('builtins.input',side_effect=['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','','y'])
    def test_result_save(self,mock_inputs):
        """
        Tests if when retrieiving a search result, that the retrieved search result equals the intial search result
        """
        output1,output2 = run()
        self.assertEqual(output1,output2)


class TestAPIRecall(TestCase):
    def setUp(self):
        self.mock = MockProductFrontEnd()
        self.aqua_output = self.mock.get_every_product('unordered','aqua',False,'sodium',False,'magnesium',False,'amyl cinnamal',False,'','')

    @patch('builtins.input', side_effect = ['n','water','n','water','y','','','','','','','y'])
    def test_a_recall(self, mock_inputs):
        """
        Tests if the runction will return the last retrieved search result if the current one returns no search results.
        The last retreieved search result is self.aqua_output and is called in the setUp function. 

        """
        output, recall = run()
        self.assertEqual('Query returns no search results', output)
        self.assertEqual(self.aqua_output, recall)

    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','','y'])
    def test_null_values_a(self,mock_inputs):
        """
        Tests if result contains no Null Values as they should have all been replaced by strings 'NotAvailable and also checks if query result matches query search.
        Testing the effectiveness of display_less_null_values function in obf_db_utils.

        """
        aqua_output,output = run()
        df=pd.DataFrame(self.aqua_output)
        result = df.isnull().values.any()
        self.assertEqual(False,result)
        self.assertEqual(aqua_output,output)




class TestDBUtils(TestCase):


    def test_empty_input_list(self):
        """
        Tests if inputting an empty result to db utils function get_products_by_ids raises a programming error.
        As the empty list formts the sql query incorrectly.
        """
        with self.assertRaises(mysql.connector.ProgrammingError) as err:
            get_products_by_ids([]) 
        self.assertEqual('Input value is an empty list',str(err.exception))

    def test_one_search_id(self):
        """
        Tests that SQL table search_results in products database only contains one row, as it should only hold one row at a time based on the most recent search.
        The function checks that an IndexError is raised as a result of formatting the query result incorrectly because it returns None.
        """
        result = fetch_results(2)
        self.assertEqual(IndexError,type(result))

    def test_verify(self):
        """
        Tests if an Exception with string containing message: 'No result found for given product ID', is raised when an incorrect product id is called in the db utils function verify_product_id
        """
        with self.assertRaises(Exception) as err:
            verify_product_id(100000)
        self.assertEqual('No result found for given product ID',str(err.exception))

    def test_verify_correct_id(self):
        """
        Tests if None is returned wen incorrect id is called in verify_product_id function in db utils
        """
        result = verify_product_id(2)
        self.assertEqual(None,result)
        



if __name__ == "__main__":
    main()
