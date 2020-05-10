import requests

url = 'http://localhost:8000/api/prog'
# url = 'http://localhost:8000/files'

f = open('factorial.ch', 'rb')

files = {'file': f}


response = requests.post(url, files=files)

print(response.status_code)
print(response.text)