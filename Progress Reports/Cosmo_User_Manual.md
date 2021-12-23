# Cosmo User Manual

## Set Up
### Requirements
- A PC or Mac computer running on a Windows, MacOS or Linux distribution
- MySQL Workbench (or another compatible SQL RDBMS)
- A Python IDE such as PyCharm or VSCode
- A Web Browser

### Import databases
First, you need to run these SQL files in MySQL Workbench:
- sql_script folder
  - `cosmo_tables.sql` (Products DB: products and ingredients tables)
  - `user_info_and_wish_list_db.sql` (Products DB: search table)
  - `user_info_and_wish_list_db.sql` (Users & Wishlist DB)
Once it is done, check that all databases were properly installed.


## Run the Cosmo Wed Application
Open you Python IDE and look in the 


## Unit Tests
### Open files
To run the  unit tests, the following files need to be open: 
- scripts folder
  - `app.py`
  - `wishlist_db_utils.py`
  - `config.py`
- sql_script folder
  - `user_info_and_wish_list_db.sql`
  - `dummy_data.sql`
- testing folder
  - `wishlist_tests.py`
  - `wishlist_main.py`

### Check credentials
Firstly, check the credentials in the `config.py` file and make sure that they match yours (i.e. the user and password match your MySQL workbench credentials.)


Secondly, open up the  user_info_and_wish_list_db.sql and dummy_data.sql scripts in your MySQL workbench and run these scripts so that the database and dummy data has been created. Don't worry if you have already created these tables, the code has been written so it will run only if it hasn't already been created. Thirdly, go on the app.py file and run it on your local computer - this file creates the connection with the API so testing will not be possible until this file has been run. Fourthly, go onto the the wishlist_tests.py file and run this file - this will run the unit tests on the wishlist functions. These unit tests are testing functions that are used in wishlist_db_utils.py and wishlist_main.py files.
  The wishlist_db_utils.py contains functions that are actually called when running our application. The wishlist_main.py, however, is a file that was created to mock the UI and mocks input in order to test the wishlist functions.
  The wishlist functions were tested primarily through the unit tests found in wishlist_tests.py and mocking input found in  wishlist_main.py. (edited) 