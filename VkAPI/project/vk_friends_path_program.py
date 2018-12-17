import requests

from project.time_limiter import TimeLimiter


class VkFriendsPathProgram:
    def __init__(self, service_token):
        self._service_token = service_token

    def get_vk_friends_path(self, id1, id2, max_time, max_depth, max_friend_count):
        time_limiter = TimeLimiter(max_time)
        path = ""
        first_id_map = {id1: None}
        first_friends_ids_set = {id1}
        second_id_map = {id2: None}
        second_friends_ids_set = {id2}

        for depth_level in range(max_depth):
            if len(first_friends_ids_set) < len(second_friends_ids_set):
                first_friends_ids_set = self._get_new_graph_layer(first_friends_ids_set, first_id_map, second_id_map,
                                                                  max_friend_count, time_limiter)
                friends_intersection = self._get_intersection(first_friends_ids_set, second_id_map)
            else:
                second_friends_ids_set = self._get_new_graph_layer(second_friends_ids_set, second_id_map, first_id_map,
                                                                   max_friend_count, time_limiter)
                friends_intersection = self._get_intersection(second_friends_ids_set, first_id_map)

            time_limiter.check_time()
            if len(friends_intersection) != 0:
                first_path_part = self._get_path_part(friends_intersection[0], id1, first_id_map)
                first_path_part.reverse()
                second_path_part = self._get_path_part(friends_intersection[0], id2, second_id_map)
                second_path_part.pop(0)
                first_path_part.extend(second_path_part)
                print("Path from first user to second:\n%s" % first_path_part)

                break
        return path

    @staticmethod
    def _get_path_part(id_from, id_to, map_to):
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

    @staticmethod
    def _get_intersection(first_friends_ids_set, second_id_map):
        """this function will find the user id presented in both graphs even if there is hidden friend in one graph"""
        friends_intersection = []
        for friend_from_first in first_friends_ids_set:
            if friend_from_first in second_id_map.keys():
                friends_intersection.append(friend_from_first)
        return friends_intersection

    def _get_new_graph_layer(self, friends_ids, source_id_map, id_map_to_compare, max_friends_limit,
                             time_limiter):
        friends_of_friend_ids = set()
        for i in friends_ids:
            friends_id_list = self._get_friends(i, max_friends_limit)
            time_limiter.check_time()
            friends_of_friend_ids.update(friends_id_list)
            self._add_to_id_map(source_id_map, friends_id_list, i)
            if len(self._get_intersection(set(friends_id_list), id_map_to_compare)) != 0:
                break
            time_limiter.check_time()
        return friends_of_friend_ids

    @staticmethod
    def _add_to_id_map(id_map, id_list, parent_id):
        for i in id_list:
            if i not in id_map:
                id_map.update({i: parent_id})

    def _get_friends(self, user_id, max_friends_limit):
        req_param = {"user_id": user_id, "access_token": self._service_token, "v": "5.52"}
        response = requests.get("https://api.vk.com/method/friends.get", params=req_param)
        resp_json = response.json()
        if "response" not in resp_json:
            return []
        friends_ids_items = resp_json["response"]["items"]
        if len(friends_ids_items) > max_friends_limit:
            return []
        return resp_json["response"]["items"]
