import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzUxMjkyOTc4fQ._lqFI7ffMAZhevgSlDfn8Mlg3X4R8s6iGmRWsQQGA-Q"
}


requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())