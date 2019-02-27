import requests
import json
from urllib.request import urlopen


API_key = 'akshardham'

def send_request(origin_address):
  """ Build and send request for the given origin and destination addresses."""
  

  request = 'https://maps.googleapis.com/maps/api/geocode/json?address='
  request  = request + origin_address + '&key=' + API_key

  jsonResult = urlopen(request).read()
  response = json.loads(jsonResult)
  #return response
  
  
  return response["results"][0]["geometry"]['location']

#print(send_request('lalapet', 'AIzaSyBK6C2_vlhw2pMEBrUdCfFsZ74HHB652cs')[])

'''
d = send_request('Secunderabad', 'AIzaSyBK6C2_vlhw2pMEBrUdCfFsZ74HHB652cs')

#d = {'results': [{'address_components': [{'long_name': 'Lalapet', 'short_name': 'Lalapet', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': 'Malkajgiri', 'short_name': 'Malkajgiri', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Secunderabad', 'short_name': 'SC', 'types': ['locality', 'political']}, {'long_name': 'Ranga Reddy', 'short_name': 'R.R. District', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Telangana', 'short_name': 'Telangana', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'India', 'short_name': 'IN', 'types': ['country', 'political']}], 'formatted_address': 'Lalapet, Malkajgiri, Secunderabad, Telangana, India', 'geometry': {'bounds': {'northeast': {'lat': 17.4426001, 'lng': 78.54571109999999}, 'southwest': {'lat': 17.433543, 'lng': 78.538272}}, 'location': {'lat': 17.4388655, 'lng': 78.5415953}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 17.4426001, 'lng': 78.54571109999999}, 'southwest': {'lat': 17.433543, 'lng': 78.538272}}}, 'place_id': 'ChIJl-5Pj9ybyzsRdCReh-gUfNA', 'types': ['political', 'sublocality', 'sublocality_level_2']}], 'status': 'OK'}
print((d["results"][0]["geometry"]['location']))

{'lat': 17.4388655, 'lng': 78.5415953}  lalapet
{'lat': 17.3762656, 'lng': 78.2988637}  gandipet
{'lat': 17.4399295, 'lng': 78.4982741}  Secunderabad

'''

# print(str(l))
# print(type(l))