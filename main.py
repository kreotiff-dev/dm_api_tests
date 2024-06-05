"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'
"""
import pprint
import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "s-test12",
#     "email": "s-test1@mm.ru",
#     "password": "123456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )


url = 'http://5.63.153.31:5051/v1/account/d9aa63f6-e357-4134-995a-f94cc9b48036'
headers = {
    'accept': 'text/plain',
}

response = requests.put(
    url=url,
    headers=headers,
)

print(response.status_code)
pprint.pprint(response.json())

response_json = response.json()
print(response_json['resource']['rating']['quantity'])
