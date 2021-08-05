import requests
from requests.auth import HTTPBasicAuth
  
# Making a get request
response = requests.get('http://192.168.0.26/snapshot.cgi',
            auth = HTTPBasicAuth('erik', 'nisse6'))
 
# print request object
print(response)
