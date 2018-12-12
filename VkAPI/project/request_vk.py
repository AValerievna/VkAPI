import requests

params = {"id": "138848299", "section": "common"}
friends = requests.get("https://vk.com/friends")
# print(friends.text)
print(friends.json)
