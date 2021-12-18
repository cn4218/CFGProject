from unittest.mock import patch
from unittest import TestCase, main
from main_products import MockProductFrontEnd, run
import pandas as pd

class TestProductFrontEnd(TestCase):
    def setUp(self):
        self.mock = MockProductFrontEnd()

    @patch('builtins.input',side_effect=['n','water','y','glycerin','n','','','','','',''])
    def test_unordered_containing_water(self,mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        self.containg_water = df['ingredients_list'].str.contains('water').sum()
        self.conatining_glycerin = df['ingredients_list'].str.contains('glycerin').sum()
        self.assertEqual(len(df),self.containg_water)
        self.assertEqual(0,self.conatining_glycerin)

    @patch('builtins.input',side_effect=['n','water','n','glycerin','y','citric acid','y','','','',''])
    def test_unordered_containing_glycerin(self,mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        containg_water = df['ingredients_list'].str.contains('water').sum()
        conatining_glycerin = df['ingredients_list'].str.contains('glycerin').sum()
        conatining_citric_acid = df['ingredients_list'].str.contains('citric acid').sum()
        self.assertEqual(len(df),conatining_glycerin)
        self.assertEqual(0,containg_water)
        self.assertEqual(len(df),conatining_citric_acid)

    @patch('builtins.input',side_effect=['n','bicarbonate de sodium','n','parfum','y','limonene','y','','','',''])
    def test_unordered_containing_parfum(self, mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        df['ingredients_list'] = df['ingredients_list'].replace('í','i')
        containg_bicarb = df['ingredients_list'].str.contains('bicarbonate de sodium').sum()
        containing_parfum = df['ingredients_list'].str.contains('parfum').sum()
        containing_limonene = df['ingredients_list'].str.contains('limonene|límonene').sum()

        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containing_parfum)
        self.assertEqual(len(df),containing_limonene)
        
    @patch('builtins.input',side_effect=['n','bicarbonate de sodium','n','geraniol','y','hexyl cinnamal','y','alcohol','n','water','n'])
    def test_unordered_bicarb(self,mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        containg_bicarb = df['ingredients_list'].str.contains('bicarbonate de sodium').sum()
        containing_geraniol = df['ingredients_list'].str.contains('geraniol').sum()
        containing_hexyl = df['ingredients_list'].str.contains('hexyl cinnamal').sum()
        containing_alcohol = df['ingredients_list'].str.contains('alcohol').sum() 
        containing_water = df['ingredients_list'].str.contains('water').sum()  
        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containing_geraniol)
        self.assertEqual(len(df),containing_hexyl)
        self.assertEqual(0,containing_alcohol)
        self.assertEqual(0,containing_water)

    @patch('builtins.input',side_effect=['y','bicarbonate de sodium','n','aqua','y','','','alcohol','y','',''])
    def test_ordered_bicarb(self, mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        df['2nd ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[1])
        df['4th ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[3])
        containg_bicarb = df['ingredients_list'].str.contains('bicarbonate de sodium').sum()
        containg_aqua = df['2nd ingredient'].str.contains('aqua').sum()
        containing_alcohol = df['4th ingredient'].str.contains('alcohol').sum()
        self.assertEqual(0,containg_bicarb)
        self.assertEqual(len(df),containg_aqua)
        self.assertEqual(len(df),containing_alcohol)

    @patch('builtins.input',side_effect=['y','aqua','y','isobutane','y','','','','','sodium tallowate','n'])
    def test_ordered_aqua(self, mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        df['1st ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[0])
        df['2nd ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[1])
        containg_aqua = df['1st ingredient'].str.contains('aqua').sum()
        containg_isobutane = df['2nd ingredient'].str.contains('isobutane').sum()
        containing_sod_tal = df['ingredients_list'].str.contains('sodium tallowate').sum()
        self.assertEqual(len(df),containg_aqua)
        self.assertEqual(len(df),containg_isobutane)
        self.assertEqual(0,containing_sod_tal)

    @patch('builtins.input',side_effect=['y','water','y','parfum','y','','','','','',''])
    def test_ordered_water(self, mock_inputs):
        output = run()
        df = pd.DataFrame(output)
        df['1st ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[0])
        df['2nd ingredient'] = df['ingredients_list'].apply(lambda x:x.split(',')[1])
        containg_water = df['1st ingredient'].str.contains('water').sum()
        containg_parfum = df['2nd ingredient'].str.contains('parfum').sum()
        self.assertEqual(len(df),containg_water)
        self.assertEqual(len(df),containg_parfum)
        
        
if __name__ == "__main__":
    main()
