import requests

# SERVICE
# API_ID, APP_ID, client_id=6782230
# Secure_key=SvheTkAtQvBdK3iYIGeG
# Service_token=93b3e1fd93b3e1fd93b3e1fdea93d49ceb993b393b3e1fdcfa1d1e60429d7b4cd2d2df3

client_id = 6782230
service_token = "93b3e1fd93b3e1fd93b3e1fdea93d49ceb993b393b3e1fdcfa1d1e60429d7b4cd2d2df3"

13490007


def get_vk_friends_path(id1, id2, max_time, max_depth, max_friend_count):
    path = ""
    first_id_map = {id1: None}
    first_friends_ids_set = {id1}
    second_id_map = {id2: None}
    second_friends_ids_set = {id2}

    for depth_level in range(max_depth // 2 + 1):
        first_friends_ids_set = get_new_graph_layer(first_friends_ids_set, first_id_map)
        friends_intersection = get_intersection(first_friends_ids_set, second_id_map)
        if len(friends_intersection) != 0:
            print("FOUND!")
            first_path_part = get_path(friends_intersection[0], id1, first_id_map)
            first_path_part.reverse()
            print(first_path_part)
            second_path_part = get_path(friends_intersection[0], id2, second_id_map)
            second_path_part.pop(0)
            print(second_path_part)
            first_path_part.extend(second_path_part)
            print(first_path_part)
            print(friends_intersection)
            break
        second_friends_ids_set = get_new_graph_layer(second_friends_ids_set, second_id_map)
        friends_intersection = get_intersection(first_friends_ids_set, second_id_map)
        if len(friends_intersection) != 0:
            print("FOUND!")
            print(friends_intersection)
            break

    print(first_id_map)
    return path


def get_path(id_from, id_to, map_to):
    path = [id_from]
    cur_key = id_from
    while True:
        if cur_key == id_to:
            break
        cur_val = map_to[cur_key]
        if cur_val is None:
            raise Exception("cannot build path from-to")
        path.append(cur_val)
        cur_key = cur_val
    return path


def get_intersection(first_friends_ids_set, second_id_map):
    friends_intersection = []
    for friend_from_first in first_friends_ids_set:
        if friend_from_first in second_id_map.keys():
            friends_intersection.append(friend_from_first)
    return friends_intersection


def get_new_graph_layer(friends_ids, id_map):
    friends_of_friend_ids = set()
    for i in friends_ids:
        friends_id_list = get_friends(i)
        friends_of_friend_ids.update(friends_id_list)
        add_to_id_map(id_map, friends_id_list, i)
    return friends_of_friend_ids


def get_friends(user_id):
    req_param = {"user_id": user_id, "access_token": service_token, "v": "5.52"}
    response = requests.get("https://api.vk.com/method/friends.get", params=req_param)
    return response.json()["response"]["items"]


def add_to_id_map(id_map, id_list, parent_id):
    for i in id_list:
        if i not in id_map:
            id_map.update({i: parent_id})


# get_vk_friends_path(13490007, 138848299, 1, 1, 1)
get_vk_friends_path(48826742, 201548436, 1, 6, 1)

# test ids:
# start: 48826742
# 6: 196695595
# 4: 201548436
# 261298587
# 190452050
