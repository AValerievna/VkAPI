from project.vk_friends_path_program import VkFriendsPathProgram

service_access_token = "93b3e1fd93b3e1fd93b3e1fdea93d49ceb993b393b3e1fdcfa1d1e60429d7b4cd2d2df3"
first_id = 48826742
second_id = 201548436
timing_sec = 10
max_search_depth = 6
friends_limit = 300

vk_program = VkFriendsPathProgram(service_access_token)
vk_program.get_vk_friends_path(first_id, second_id, timing_sec, max_search_depth, friends_limit)
