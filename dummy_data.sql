use cfg_project;
select * from wish_list;
select * from user_info;

call cfg_project.fill_user_info(1, '@nasian', 'nasian', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 1 );

call cfg_project.fill_user_info(2, '@nasianahmed', 'nasianahmed', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 2 );

call cfg_project.fill_user_info(3, '@nasiana', 'nasianahmed', 'nasian@gmail.com');
call cfg_project.fill_wish_list( 2, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 3 );
call cfg_project.fill_wish_list( 1, 101, 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz', 'xyz','xyz', 'xyz', 'xyz', 3 );