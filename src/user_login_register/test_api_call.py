import requests

url = "http://127.0.0.1:8000/user_login_register/"
headers = {
    "Authorization": "Token 575e2eb26b666704748e72ffa742fca543ed1a9d"
}

r = requests.get(url, headers=headers)
print(r)
