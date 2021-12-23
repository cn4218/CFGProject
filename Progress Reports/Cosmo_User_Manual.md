# Cosmo User Manual

## Set Up
### Requirements
- A PC or Mac computer running on a Windows, MacOS or Linux distribution
- MySQL Workbench (or another compatible SQL RDBMS)
- A Python IDE such as PyCharm or VSCode
- A Web Browser
- Make sure that the following Python packages are installed:
  - `mysql.connector` to connect to SQL DBs
  - `flask` micro web application framework
  - `flask-cors` Cross Origin Resource Sharing (CORS): required for the frontend to send requests
  - `json` used to write the API
  - `requests` used to write the API
  - `pandas` used to clean up the OBF DB
  - `numpy` used to create functions in the `ListDF.py` homemade module
  - `ListDF.py` (homemade module to apply functions on whole dataframe columns)
  - `pprint` to display messages to the terminal while debugging/testing
  - `unittest` for testing
  - `unittest.mock` for testing
  - `operator` for testing
  - `sys` to add folders to the Python path so other scripts can be imported

### Import and set up databases + config files
- First, you need to run these SQL files in MySQL Workbench:
  - sql_script folder
    - `cosmo_tables.sql` (Products DB: products and ingredients tables)
    - `user_info_and_wish_list_db.sql` (Products DB: search table)
    - `user_info_and_wish_list_db.sql` (Users & Wishlist DB)
  Once it is done, check that all databases were properly installed.
- Then the password for your MySQL Workbench connection should be assigned to the PASSWORD variable in the `config.py` file

## Run the Cosmo Web Application
1. Open you Python IDE and run the `app.py` file in the `scripts` folder
2. Go to the `log_in.html` file in the `frontend` folder and open the file in a web browser
3. The webpage will prompt you to enter your username and email; please enter the following credentials:
   - Username - sample_name
   - Email Address - sample@gmail.com
4. This will lead you to the `Home`/`Search` page where you can run searches for different ingredients and review the results under the `Results` tab. 
5. You can also add specific products to your wishlist by inserting their productID at the top of the page and clicking on the button "add to wishlist". 
6. Everything you add to the wishlist can be viewed on the `Wishlist` tab.


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
First, check the credentials in the `config.py` file and make sure that they match yours (i.e. the user and password match your MySQL workbench credentials.)


Secondly, open up the  user_info_and_wish_list_db.sql and dummy_data.sql scripts in your MySQL workbench and run these scripts so that the database and dummy data has been created. Don't worry if you have already created these tables, the code has been written so it will run only if it hasn't already been created. Thirdly, go on the app.py file and run it on your local computer - this file creates the connection with the API so testing will not be possible until this file has been run. Fourthly, go onto the the wishlist_tests.py file and run this file - this will run the unit tests on the wishlist functions. These unit tests are testing functions that are used in wishlist_db_utils.py and wishlist_main.py files.
  The wishlist_db_utils.py contains functions that are actually called when running our application. The wishlist_main.py, however, is a file that was created to mock the UI and mocks input in order to test the wishlist functions.
  The wishlist functions were tested primarily through the unit tests found in wishlist_tests.py and mocking input found in  wishlist_main.py. (edited) 