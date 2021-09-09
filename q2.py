import requests

q2 = requests.get('https://github.com/jsmith465264/cmput404Lab/blob/main/q2.py')
print(q2.content)
