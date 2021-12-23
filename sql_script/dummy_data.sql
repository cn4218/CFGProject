use cfg_project;

-- Notes for the instructor:
-- Make sure to add dummy data through this dummy data file as the testing functions rely on the dummy data, please run this
-- dummy data SQL file before running wishlist_tests.py. Ideally, add this dummy data before running the application and adding
-- further data yourself, as this will interfere with my tests. But regardless, the tests should run and you can see
-- the differences as a result of records you've added yourself. Alternatively, you could drop the cfg_project schema,
-- then rerun the user_info_and_wish_list_db.sql script to create the database and tables from scratch, then run the 
-- dummy_data.sql to create the dummy data from scratch - then finally run wishlist_tests.py and the tests should be able to run

-- Run the following stored procedures in order to be able to run the tests for the wish list 
-- The following stored procedures create dummy data which are crucial for both main and unit tests and serve to test the wishlist

call cfg_project.fill_user_info(1, '@nasian', 'nasian', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 1 );
call cfg_project.fill_wish_list(3, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 1 );


call cfg_project.fill_user_info(2, '@nasianahmed', 'nasianahmed', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 1, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 2 );
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 2 );
call cfg_project.fill_wish_list( 3, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 2 );


call cfg_project.fill_user_info(3, '@nasiana', 'nasianahmed', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 1, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 3 );
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 3 );

select * from wish_list where user_id = 2;