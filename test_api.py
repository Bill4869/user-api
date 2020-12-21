import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld/b/25")



response = requests.get(BASE + "user/1")
print(response.json())
input()

response = requests.put(BASE + "user/1", {"name": "B"})
print(response.json())

input()

response = requests.put(BASE + "user/1", {"name": "B", "sex": "M"})
print(response.json())

input()

response = requests.patch(BASE + "user/1", {"sex": "F", "age": 25})
print(response.json())


# response = requests.delete(BASE + "user/1")
# print(response)

# response = requests.get(BASE + "user/1")
# print(response.json())