from unittest.mock import patch
from unittest import TestCase, main
from main_products import MockProductFrontEnd, run
from obf_db_utils import _get_all_product_ids, get_productids_containing, get_products_by_ids, fetch_results
import pandas as pd
from operator import *
import mysql.connector

class TestAPIProductFrontEnd(TestCase):
    def setUp(self):
        self.mock = MockProductFrontEnd()

    @patch('builtins.input',side_effect=['n','water','y','glycerin','n','','','','','','',''])
    def test_unordered_containing_water(self,mock_inputs):
        output,_ = run()
        df = pd.DataFrame(output)
        self.containg_water = df['ingredients_text'].str.contains('water').sum()
        self.conatining_glycerin = df['ingredients_text'].str.contains('glycerin').sum()
        self.assertEqual(len(df),self.containg_water)
        self.assertEqual(0,self.conatining_glycerin)

    @patch('builtins.input',side_effect=['n','water','n','glycerin','y','citric acid','y','','','','',''])
    def test_unordered_containing_glycerin(self,mock_inputs):
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
        output,_ = run()
        df = pd.DataFrame(output)
        df['1st ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[0])
        df['2nd ingredient'] = df['ingredients_text'].apply(lambda x:x.split(',')[1])
        containg_water = df['1st ingredient'].str.contains('water').sum()
        containg_parfum = df['2nd ingredient'].str.contains('parfum').sum()
        self.assertEqual(len(df),containg_water)
        self.assertEqual(len(df),containg_parfum)

    @patch('builtins.input',side_effect = ['n','water','y','water','n','','','','','',''])
    def test_bad_input(self,mock_inputs):
        output,_ = run()
        self.assertEqual('Query returns no search results',output)


    @patch('builtins.input',side_effect = ['y','water','y','Stearalkonium chloride','y','stearyl alcohol','y','butyrospermum parkii (beurre de karité)','n','caprylic/capric triglyceride','n'])
    def test_bad_input_result(self,mock_inputs):
        output,_ = run()
        self.assertEqual('Query returns no search results',output)


    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','',''])
    def test_allergic_to_ingredients_aqua(self,mock_inputs):
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
        output,_ = run()
        df = pd.DataFrame(output)
        containing_water = df['ingredients_text'].str.contains('water').sum()
        result_all = _get_all_product_ids()
        result_water = get_productids_containing('water')
        expected_length = len(result_all)-len(result_water)
        self.assertEqual(0,containing_water)
        self.assertEqual(len(df),expected_length)

    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','','y'])
    def test_null_values(self,mock_inputs):
        self.aqua_output,output = run()
        df=pd.DataFrame(self.aqua_output)
        result = df.isnull().values.any()
        print(result)
        self.assertEqual(False,result)
        self.assertEqual(self.aqua_output,output)

    @patch('builtins.input',side_effect = ['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','',''])
    def test_null_values_order(self,mock_inputs):
        output,_ = run()
        occurence_na = []
        for item in output:
            count_occ = countOf(item.values(), 'NotAvailable')
            occurence_na.append(count_occ)      
        print(occurence_na)

        self.assertEqual(occurence_na,sorted(occurence_na))

    @patch('builtins.input',side_effect=['n','aqua','n','sodium','n','magnesium','n','amyl cinnamal','n','','','y'])
    def test_result_save(self,mock_inputs):
        output1,output2 = run()
        self.assertEqual(output1,output2)


class TestDBUtils(TestCase):


    def test_empty_input_list(self):
        with self.assertRaises(mysql.connector.ProgrammingError) as err:
            get_products_by_ids([]) 
        self.assertEqual('Input value is an empty list',str(err.exception))

    def test_one_search_id(self):
        with self.assertRaises(IndexError) as err:
            fetch_results(2)
        self.assertEqual('Query returns no search results, use search ID 1',str(err.exception))


    







if __name__ == "__main__":
    main()
