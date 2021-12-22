use cfg_project;

select * from user_info;
select * from wish_list;

-- run the following stored procedures in order to be able to run the tests for the wish list 
-- the foollowing stored procedures create dummy data which are crucial for both main and unit tests and serve to test the wishlist

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

