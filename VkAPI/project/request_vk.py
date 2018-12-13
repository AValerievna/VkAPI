import requests

# SERVICE
# API_ID, APP_ID, client_id=6782230
# Secure_key=SvheTkAtQvBdK3iYIGeG
# Service_token=93b3e1fd93b3e1fd93b3e1fdea93d49ceb993b393b3e1fdcfa1d1e60429d7b4cd2d2df3

client_id = 6782230
service_token = "93b3e1fd93b3e1fd93b3e1fdea93d49ceb993b393b3e1fdcfa1d1e60429d7b4cd2d2df3"

13490007


def get_path(id1, id2, max_time, max_depth, max_friend_count):
    path = ""
    req_param = {"user_id": id1, "access_token": service_token, "v": "5.52", }
    response = requests.get("https://api.vk.com/method/friends.get", params=req_param)
    data = response.json()
    print(data)
    return path


get_path(13490007, 1, 1, 1, 1)
