import requests

google = requests.get('http://google.com/')
print(google.content)
