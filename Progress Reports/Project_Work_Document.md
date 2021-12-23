# <center>Project Work Document – Group 2 <br><small>Cosmo – Cosmetics Search engine by Ingredients</small></center>

<!-- Below is a draft structure for your project document submission. Sections in bold font are compulsory, however you may adjust any sub-sections (remove or add) as required to make it tailored to your own work.
This document would be used to assess your project work and understand your approach to the project delivery. It will also provide an insight into your architecture, testing and implementation strategy as a team.

NOTE: Your instructors team would also use this documents as part of the mock interview assessments to support their enquiries about your work and ‘rehearse’ live-like interview scenarios.
We expect this report to be concise, but very detailed, so that every key point is explained and covered. It should be no more than 5-7 pages (A4) long. The report can and should include diagrams, images with descriptive captions.-->

## INTRODUCTION
### Aims and objectives of the project
Our project aimed at building a cosmetic search engine by ingredient: Cosmo.  
Our objectives were to allow users to: 
- sign up, create an account and log in to it (Users side) <!--arm/wing-->
- search for products meeting several ingredient-related criteria (Products side)
- save selected products to their wishlist and manage it as they want (Wishlist side)

### Roadmap of the report
xxxxxxxxxxxxxxxxxxxxxxxxxxx


## BACKGROUND
<!--Any specific details about the project based on your chosen topic. For example, if it is a game, it would be good to understand the rules of the game and its logic. If it is a trading portfolio, then explain what analysis you are performing (end of day profit/loss, historical price evaluation etc.) and how does it work. If it is a restaurant booking system, then explain the rules / requirements that your team locked in for the system.-->

Imagine looking for a replacement to your favourite conditioner which has been discontinued, a cheaper equivalent to some expensive skincare product, one excluding some ingredients to which you are allergic, or substituting them by more ethical alternatives. How would you go about it?

The world of cosmetics can be difficult to navigate: marketing often presents products as some sort of magic potions wrapped in a pretty packaging, using fancy buzzwords and making inaccurate and/or unrealistic claims about their benefits.  

In reality, cosmetics are formulas composed of specific molecules with a particular biological effect, and even though their exact recipe remains a trade secret, the order of ingredients on the label reveals important information, as it reflects their relative concentrations: the first has the highest concentration, the last one the lowest.

In theory, an informed user should thus be able to make a choice based on this objective criteria. Given the host of choice we are given on the market, however, this deceptively simple task can prove nigh impossible. One cannot realistically browse the entire web, systematically comb every shop shelf and read every single product label… This is where data comes into play at our rescue.

Some cosmetic-related tools and search engines such as Open Beauty Facts (OBF) or INCIDecoder already exist, but so far they only offer a list of products containing or not a specific ingredient, regardless of their position within the list.

Cosmo is an app that not only returns a list of products containing a particular ingredient, but also takes into account its position in the ingredient list. Moreover, it allows you to search for products without a specific ingredient, and to perform a multi-criteria search up to the 5<sup>th</sup> ingredient.


## SPECIFICATIONS AND DESIGN
### Requirements 
#### Technical requirements 
We used portable tools and languages to build our application, specifically:
- Languages: Python 3.9, SQL, javascript, html and css
- RDBMS: MySQL Workbench and DB Browser for SQLite
- IDEs: PyCharm and VSCode
- Version Control: GitHub.com and IDEs Git tools

#### Non-technical requirements
We strove to follow the Software Development Life Cycle (SDLC) framework and to implement Agile methodology. In particular, we had our Scrum Master organise Daily Scrum and weekly Sprint Planning meetings on Zoom. We also created "User Stories" to present features to implement in our product. We started by creating a very minimal core app with only a few functions, made sure that they worked, then incrementally improved our app.
A ClickUp workspace was also for our group to help us organise our tasks.

### Design and architecture
Our application comprises the following components, here ordered from the back end to the front end:
- **2 Databases**
  - Products DB
    - Products table
    - Ingredients table
    - Search table
  - Users & Wishlist DB
    - Users table
    - Wishlist table
- **3 DB Utils scripts**
  - For Products
  - For Users (OOP)
  - For Wishlists 
- **API (2-in-1)**
  - Products API
  - Users & Wishlist API
- **Website User Interface (UI)**
  - Home page/ Search Tool
  - Login and Sign up page
  - Results display page
  - Login and Sign up page
  - Wishlist page
  - Account page

![Cosmo_Diagram_3.png](Cosmo_Diagram_3.png)  
<div style="text-align: right"> High-level Diagram of the Cosmo application</div>

#### Databases (DB)
Because we originally planned to use the remote Open Beauty Facts products DB through their API and to create our own Cosmo DB containing Users information and their Wishlists, we decided to keep the "Products" and the "Users & Wishlist" DB artificially separated. In reality, this is not absolutely necessary, and we could put them together, but we kept them apart in order to conserve our original design with an external and an internal DB. For this project, they are still run on the same local RDBMS, but ultimately we would like to host them on a remote server . 

![Cosmo_EER_Diagram.png](Cosmo_EER_Diagram.png)  
<div style="text-align: right">Databases EER diagram</div>

##### 1 - Products DB (`cosmo_tables.sql` and `Products` DB)
The `Products` database, also referred to as `OBF DB`, contains cosmetic products related information and is divided into two large `products_table`and `ingredients_table` and a smaller `search_products`table.

###### Products table (`products_table`)
The product table is a cleaned up version of the database downloaded from [Open Beauty Facts](https://world.openbeautyfacts.org/data/en.openbeautyfacts.org.products.csv). This 18843 rows x 176 columns table was modified by the `clean_csv_tables.py` script using the `pandas` library and a homemade `ListDF.py` module in order to only keep products for which a proper list of ingredients was available. A unique `productID` was created for each row and only 17 columns were selected, resulting in a 7082 rows x 18 columns table. A monotonically increasing `index` field was also added because as the database was being cleaned up, some rows were deleted but the others kept the same `productID` for consistency. *(see EER diagram above)*  

###### Ingredients table (`ingredients_table`)
The `ingredients_text` column from the products table was then parsed, transformed into a list and expanded, so that for each `productID`, every single ingredient would go into a single column according to its index in the list. This step created a new 7082 rows x 119 columns table in which the first field corresponds to the productID, and the others to the index of ingredients within the ingredients list, from `0` to `117`. *(see EER diagram above)*  


###### Search table (`search_table`)
This table temporarily (?) stores the results of individual product searches so that they can be retrieved and displayed on the Results web page while doing another search. *(see EER diagram above)*


##### 2 - Users & Wishlist DB (`CFG_Projet`)
###### Users information table (`Users_Info`)

###### Wishlist table (`Wish_List`)


#### DB Utils (+ credentials)
##### 3 - For products (`obf_db_utils.py` + `config.py`)
This file will contain functions responsible for querying the DB. Some of these functions will get the productIDs corresponding to the ingredients the user requested and fetch the product info linked to those ID’s. This search could either be done in an ordered way where ingredients must be in a fixed position in the ingredient list or in an unordered way. Another function to include would be one searching for products that do not contain a particular ingredient or set of ingredients.

**Functions in this file**  
- `_connect_to_db(db_name)`
- `_map_values(result)`
- `exception_handler(query)`
- `get_productids_containing(ingredient,n=None)`
- `get_productids_ingt_in_nth_position(ingredient, n)`
- `get_products_by_ids(id_list)`
- `format_input(ingredients_input)`
- `get_products(output,search_func1,search_func2)`
- `get_proper_ingredients_list(_dict)`
- `_get_all_product_ids`
- `display_less_null_values`
- `store_results`
- `fetch_results`
- `returning_products_in_pages`


##### 4 - For users (OOP) (`db_utils_user_oop.py` + `config.py`?)
**Methods in this file**
**`class dbConnection`**
- `__init__(self)`
- `conn(self)`
- `add_user(self, user_id)`
- `_get_user(self, user_id)`
- `update_user(self)`
- `delete_user(self)`
- `verify_login(self, user_id, username, name_user, email_address)`
- `get_user_id(self, username, name, email)`


##### 5 - For wishlists (`wishlist_db_utils.py` + `wishlist_config.py`)
This file will contain functions responsible for querying the database and handling db connection errors if they occur. Some of these functions will insert user info into the user info table and retrieve it whenever the user logs in, other functions will either insert or retrieve wishlist data and are used depending on the nature of the API request.

**Functions in this file**


#### 2-in-1 API (`app.py`)
Our Flask RESTful 2-in-1 API creates routes (http pipeline) for data exchange by offering endpoints to connect to our 2 databases from the website UI with which the user interacts.

A few of the operations will include but are not limited to:
- Use the user's product ingredient search to query the Products DB
- Send the results from this query to be displayed on the Results display webpage
- Transfer new wishlist data from the website to the wishlist table in the User Info DB
- Send all the wishlist data from the wishlist table to the website whenever the user wants to view them on the wishlist page

The API is primarily responsible for creating the routes (http pipeline) for this data exchange and the bulk of the operations listed above is handled by the DB_utils files we will discuss below.

##### 6 - Products API ()


##### 7 - Users & Wishlist API ()

#### Website User Interface (UI)

##### Home page/ Search Tool
As the system is designed around searching for ingredients that already exist, one of its key features is the search tool. Shows input fields for up to 5 ingredients.
Can search for ingredients to be done in the unspecified order:
We designed this tool to search a database that lists all the specific ingredients in beauty products and return results where specified ingredients appear.
We also designed the opposite feature, so the search results in only products without certain ingredients. For example, if a searcher was allergic to ingredient x, all products containing ingredient x would be removed from all of their search results.

Or in the specified order: Another feature of the search tool is the ability to search for an ingredient in a specific position on a product’s ingredient list. Generally, in beauty products, ingredients are listed in order of what has been used most, so our tool enables searchers to look for ingredients with a larger percentage of each ingredient.

##### Login and Sign up page
New users can sign up for an account and old users can just log into their previously created account at any time.

##### Results display page
This is where the users search results will be displayed according to the ingredients they put in on the home page.

##### Login and Sign up page
New users can sign up for an account and old users can just log into their previously created account at any time.

##### Wishlist page
Another important component of the system is a wishlist which enables users to save products from their search results. When a user likes a particular product from the search results page, they have the option to add it to the wishlist. Any product added to the wishlist will be stored and displayed on the wishlist page. This relies on the creation of an account which would store all products specified by the user. Each wishlist is unique to the user, and stores only the products they have selected from their own search results.

##### Account page
Shows the user's personal information such as their username, email address, etc.



## IMPLEMENTATION AND EXECUTION
### Development approach and team member roles
We tried to give ourselves roles as in a typical Agile team, but as we all had the same experience with this methodology (that is, none), it was not really possible to rely on a senior Agile expert "Scrum Master", and the role of "Product Owner" was also difficult to implement in a self-organising "democratic" team. Therefore, the workload was distributed based on the sections on which team members wanted to work, because they enjoyed this particular part of the project or in order to improve these particular programming skills.

|                **TASKS**                |**Chizu**|**Claire**|**Georgia**|**Nasian**|**Nikita**|**Sophie**|
| :-------------------------------------- | :-----: | :------: | :-------: | :------: | :------: | :------: |
| Products DB (Cosmo-OBF)                 |    X    |     X    |           |          |          |          |
| Users & Wishlist DB                     |         |          |     X     |     X    |     X    |          |
| Products DB_Utils & Config              |    X    |     X    |           |          |          |     X    |
| Users DB_Utils & Config                 |         |          |     X     |     X    |     X    |          |
| Wishlist DB_Utils & Config              |         |          |           |     X    |     X    |     X    |
| Products API                            |    X    |     X    |           |          |          |          |
| Users & Wishlist API                    |         |          |           |          |     X    |     X    |
| Tests                                   |         |          |           |     X    |          |     X    |
| Backend Main (mock Front End for tests) |         |          |           |          |          |     X    |
| Front End Web UI                        |    X    |          |     X     |          |          |          |
| Documentation, organisation             |    X    |     X    |           |          |          |          |
| *Scrum Master*                          |    x    |          |     x     |          |          |          |
| *Product Owner*                         |         |     x    |           |          |          |          |

### Tools and libraries
- `mysql.connector`
- `flask`
- `flask-cors`
- `json`
- `requests`
- `pandas`
- `math`
- `unittest`
- `unittest.mock`
- `operator`
- `ListDF.py` (homemade module to apply functions on whole dataframe columns)

### Implementation process (achievements, challenges, decision to change something)
Originally, we intended to use the Open Beauty Facts (OBF) DB indirectly by consuming their API, but as it was still very experimental, barely documented, and did not actually work for our purpose since it only offered the possibility to search for products barcodes, we changed our minds and resolved to use the OBF database differently.  
At the beginning, we even considered webscraping it, but it was not practical, and eventually we settled for downloading it as a CSV file. We then cleaned it up to obtain the `products_table` table, which was then used to create the `ingredients_table` table. As some of us ran through codec errors preventing the these files from being normally imported into MySQL Workbench, it was done into DB Browser for SQLite instead. The resulting `Products` database was eventually exported as a SQL file, then imported back into MySQL Workbench and its syntax slightly modified to function on this RDBMS.

### Agile development (did team use any agile elements like iterative approach, refactoring, code reviews)

### Implementation challenges
One of the main challenges we had to overcome was actually the coordinated use of GitHub. 

## TESTING AND EVALUATION
### Testing strategy
We intend to test the system using unit testing for various aspects of our code and system.

#### Test Files

- `obf_main.py`
  - **`class MockProductFrontEnd`**
    - `get_every_product(self,order,ingredient1,boolean1,ingredient2,boolean2,ingredient3,boolean3,ingredient4,boolean4,ingredient5,boolean5)`
    - `fetch_existing_search_result(self)`
    - `welcome_message(self)`
    - `selecting_ingredients(self)`
    - `input_products(self)`
    - `results_again(self)`
    - `run()`  


- `obf_tests.py`
  - **`class TestAPIProductFrontEnd(TestCase)`**
    - `setUp(self)`
    - `test_unordered_containing_water(self,mock_inputs)`
    - `test_unordered_containing_glycerin(self,mock_inputs)`
    - `test_unordered_containing_parfum(self, mock_inputs)`
    - `test_unordered_bicarb(self,mock_inputs)`
    - `test_ordered_aqua(self, mock_inputs)`
    - `test_ordered_water(self, mock_inputs)`
    - `test_bad_input(self,mock_inputs)`
    - `test_bad_input_result(self,mock_inputs)`
    - `test_allergic_to_ingredients_aqua(self,mock_inputs)`
    - `test_allergic_to_ingredients(self,mock_inputs)`
    - `test_no_water(self, mock_inputs)`
    - `test_null_values(self,mock_inputs)`
    - `test_null_values_order(self,mock_inputs)`
    - `test_result_save(self,mock_inputs)`
  - **`class TestDBUtils(TestCase)`**
    - `test_empty_input_list(self)`
    - `test_one_search_id(self)`


TEST CASES `obf_tests.py`:
- Ordered ingredients input
- Unordered ingredients input
- Input that returns no results
- Input with only ingredients not wanted
- Tests no null values in output
- Tests product dictionaries with more null values appear at bottom of results
- Tests retrieving most recent search result brings back exact same result
- Tests exception handling in obf db utils


- `user_main.py`
  - **`class MockFrontEnd`**
    - `__init__(self)`
    - `get_profile_by_id(self,user_id)`
    - `add_new_user(self,user_name,name,email)`
    - `delete_user_func(self,user_id)`
    - `user_login(self,user_name,email)`
    - `welcome_message(self)`
    - `enter_details(self)`
    - `verify_account_added(self)`
    - `displaying_user(self)`
    - `deleting_account(self)`
    - `run()`


- `user_tests.py`
  - **`class TestApiDb(TestCase)`**
    - `setUp(self)`
    - `test_add_new_user(self)`
    - `test_add_new_user_2(self)`
    - `test_get_fang_profile(self)`
    - `test_add_new_user_has_been_added(self)`
    - `test_deleting_user(self)`
    - `test_user_login(self)`
    - `test_user_login_false(self)`
    - `test_delete_non_existing_user(self)`
  - **`TestMockFrontEnd(TestCase)`**
    - `test_positive_input(self, mock_input)`
    - `test_negative_input(self, mock_input)`
    - `test_wrong_input(self, mock_inputs)`
    - `test_incorrect_email(self, mock_inputs)`
    - `test_incorrect_email_2(self, mock_inputs)`
    - `test_adding_user(self,mock_inputs)`
  - **`class TestRunFunction(TestCase)`**
    - `test_incorrect_email_3(self,mock_inputs)`
    - `test_creating_user(self,mock_inputs)`
    - `test_deleting_user(self,mock_inputs)`
    - `test_creating_user2_ayesha(self,mock_inputs)`
    - `test_creating_user_zita(self,mock_inputs)`
    - `test_goodbye(self,mock_input)`
  - **`TestUsersDelete(TestCase)`**
    - `setUp(self)`
    - `test_delete_zita_user(self)`
    - `test_delete_fang_user(self)`
    - `test_delete_sophie_user(self)`
    - `test_delete_ayesha_user(self)`
    - `test_delete_unknown_id(self)`


- `wishlist_main.py`
  - **`class MockFrontEnd`**
    - `__init__(self, db_name)`
    - `def add_new_wishlist(self)`
    - `_get_wish_list_individual(self, User_ID, productID)`
    - `_get_wish_list_all(self, User_ID)`
    - `delete_wishlist_item(self, User_ID, productID)`
    - `delete_wishlist(self, User_ID)`
    - `welcome_message(self)`
    - `verify_wish_list_item(self)`
    - `verify_wish_list(self)`
    - `deleting_wishlist_item(self)`
    - `deleting_wishlist(self)`
    - `run()`


- `wishlist_tests.py`
  - `class TestWishListApiDb(unittest.TestCase)`
    - `test_1_add_wish_list(self)`
    - `test_2_get_wish_list_item_if_not_exists(self)`
    - `test_3_get_wish_list_all_if_not_exists(self)`
    - `test_4_delete_wish_list_item_if_not_exists(self)`
    - `test_5_delete_wish_list_all_if_not_exists(self)`
    - `test_6_get_wish_list_item_if_exists(self)`
    - `test_7_get_wish_list_all_if_exists(self)`
  - `class TestMockFrontEnd(unittest.TestCase)`
    - `setUp(self)`
    - `test_8_add_new_wishlist(self)`
    - `test_9_verify_wish_list_item(self, mock_inputs)`
    - `test_10_verify_wish_list(self, mock_inputs)`
    - `test_11_add_new_wishlist_mocked_values(self, mock_wish_list_dict)`
  - `class TestMockFrontEndDelete(unittest.TestCase)`
    - `setUp(self)`
    - `test_12_delete_wish_list_item(self, mock_inputs)`
    - `test_13_delete_wish_list_all(self, mock_inputs)`
  - `class ReAddingData(unittest.TestCase)`
    - `test_14_re_add_mock_wish_list(self)`
    - `test_15_re_add_wish_list_1(self)`
    - `test_16_re_add_wish_list_2(self)`
  - `class TestWishListApiDbDeletingUsers(unittest.TestCase)`
    - `test_17_delete_wish_list_item(self)`
    - `test_18_re_add_wish_list(self)`
    - `test_19_delete_wish_list_all(self)`
    - `test_20_re_add_wish_list_1(self)`
    - `test_21_re_add_wish_list_2(self)`

### Functional and user testing
we want to test:
- The creation of a new user account in which the user will input their name, email and password - to make sure this information is both updated to the sql database and actually creates an account for the user to login to.
- We want to test our data and ensure we can get information associated with a specific user through their user ID/ name - one way would be to have a Test case ID to ensure all users have a unique ID to represent them
- We want to test the searching facility to make sure ingredients are found in the correct order.
- We also expect to test the ability of our system to retrieve and display items with a specific ingredient defined by the user.
- We want to test the wishlist feature to make sure all items on the wish-list are displayed qon the wishlist page, with a dictionary containing product information. This test would also need to show that the items a user saves in their wishlist basket is also updated to a SQL database so that the user is able to retrieve their saved wishlist items at a later date.

### System limitations


## CONCLUSION