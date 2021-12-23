# <center>Cosmo User Manual</center>

## Set Up
### Requirements
- A PC or Mac computer running on a Windows, MacOS or Linux distribution
- MySQL Workbench (or another compatible SQL RDBMS)
- A Python IDE such as VSCode (recommended) or PyCharm
- The live server extension for VSCode ([Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) or PyCharm ([Live Edit](https://www.jetbrains.com/help/pycharm/live-editing.html)) so that you can run your html script on your browser.
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
  - `pathlib` to add folders to the Python path so other scripts can be imported
  - `sys` to add folders to the Python path so other scripts can be imported

### Import and set up databases + config files
1. First, you need to run these SQL files in MySQL Workbench:
  - sql_script folder
    - `cosmo_tables.sql` (Products DB: products and ingredients tables)
    - `temp_search_results.sql` (Products DB: search table)
    - `user_info_and_wish_list_db.sql` (Users & Wishlist DB)
  Once it is done, check that all databases were properly installed.
2. Then the password for your MySQL Workbench connection should be assigned to the PASSWORD variable in the `config.py` file

### Clone GitHub repository
Clone this [GitHub repository](https://github.com/cn4218/CFGProject) in your Python IDE, preferably VSCode, and checkout the `temp_v3_branch`



## Run the Cosmo Web Application
1. Open you Python IDE and run the `app.py` file in the `scripts` folder
2. Go to the `log_in.html` file in the `frontend` folder and open the file in a live server. 
3. The webpage will prompt you to enter your username and email; please enter the following credentials:
   - Username - `sample_name`
   - Email Address - `sample@gmail.com`
4. This will lead you to the `Home`/`Search` page where you can run searches for different ingredients and review the results under the `Results` tab. 
5. You can also add specific products to your wishlist by inserting their productID at the top of the page and clicking on the button "add to wishlist". 
6. Everything you add to the wishlist can be viewed on the `Wishlist` tab.

*** 
## Unit Tests
### 1. Open files
To run the unit tests, first open the following files: 
- scripts folder
  - `app.py`
  - `wishlist_db_utils.py`
  - `user_db_utils.py`
  - `config.py`
- sql_script folder
  - `user_info_and_wish_list_db.sql`
  - `dummy_data.sql`
- testing folder
  - `wishlist_tests.py`
  - `wishlist_main.py`
  - `user_tests.py`
  - `user_main.py`
  - `obf_tests.py`
  - `obf_main.py`

### 2. Check credentials
Check the credentials in the `config.py` file and make sure that they match yours (i.e. the user and password match your MySQL workbench credentials.)

### 3. Create Users & Wishlist DB with dummy data
Open the `user_info_and_wish_list_db.sql` and `dummy_data.sql` scripts in MySQL Workbench and run these scripts so that the database and dummy data are created. Don't worry if you have already created these tables, the code is written to run only if the database does not already exist. 

### 4. Run the app
Run the `app.py` file on your Python IDE and keep it running whilst running the tests. This file creates the connection with the API, so testing will only be possible once this file has been run. 

### 5. Run the tests
#### Wishlist Tests
Run the `wishlist_tests.py` file. This will run unit tests on the wishlist functions used in the `wishlist_db_utils.py` and `wishlist_main.py` files.  
The `wishlist_db_utils.py` contains functions called when running our application.  
The `wishlist_main.py`, however, is a file created to mock the UI and user inputs in order to test wishlist functions.  
Wishlist functions are primarily tested through the unit tests found in `wishlist_tests.py` and mocking input found in `wishlist_main.py`. 

#### Users Tests
Run the `user_tests.py` file. This will run unit tests on the user functions used in the `user_db_utils.py` and `user_main.py` file.
The `user_db_utils.py` contains functions called when running our application.  
The `user_main.py`, however, is a file created to mock the UI and user inputs in order to test user functions.  
User functions are primarily tested through the unit tests found in `user_tests.py` and mocking input found in `user_main.py`.

#### Products Tests
Run the `obf_tests.py` file. This will run unit tests on the products functions used in the `obf_db_utils.py` and `obf_main.py` file.
The `obf_db_utils.py` contains functions called when running our application.  
The `obf_main.py`, however, is a file created to mock the UI and products inputs in order to test products functions.  
Products functions are primarily tested through the unit tests found in `obf_tests.py` and mocking input found in `obf_main.py`.
 the testing folder