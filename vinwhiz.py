import requests

url = 'https://apitesting.vinwhiz.com/api/v1.1/vins/1GYS4HKJXHR376823/ris'

api_key = '2D979E71-EE01-4B7D-A995-F2A2D29A5E85'

r = requests.get(url, headers={"api-key": f"{api_key}", "accept": "application.json"})
