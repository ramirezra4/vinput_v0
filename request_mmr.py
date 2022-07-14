import requests

base_url = 'http://cloud.jdpower.ai/data-api/valuationservices/valuation/vehiclesByVin'

params = {'api-key': 'ee9b1fc6-f3fc-4f14-ae88-2fcb02d2e3ab', 'accept': 'application/json'}

r = requests.get(base_url, headers=params)
print(r)