# import gphoto2cffi as gp
import requests
import json
import ssdp
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

response = ssdp.discover()
for item in response.split('\n'):
    if 'LOCATION' in item:
        location_url = item.strip().split(' ')[1] #get location url fron ssdp response
device_xml_request = requests.get(location_url)
xml_file = str(device_xml_request.content.decode())

xml = ET.fromstring(xml_file)
device_tag = xml.find('{urn:schemas-upnp-org:device-1-0}device')
api_info = device_tag.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo')
api_version = api_info.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_Version').text
service_list = api_info.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceList')
print(api_version)
api_service_urls = {}
for service in service_list:
    service_type = service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType').text
    action_url = service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ActionList_URL').text
    api_service_urls[service_type] = action_url
print(api_service_urls)

# TODO: make python wrapper class: libsony, connection, call
def start_rec():
    endpoint_url = api_service_urls['camera'] + '/camera'
    json_request= {
     "method": "startRecMode",
     "params": [],
     "id": 1,
     "version": "1.0"
    }
    request = requests.post(endpoint_url, json.dumps(json_request))
    print(json.loads(request.content))
def set_remote():
    endpoint_url = api_service_urls['camera'] + '/camera'
    json_request = {
         "id": 1,
         "method": "setCameraFunction",
         "params": [
         "Remote Shooting"
         ],
         "version": "1.0"
        }
    request = requests.post(endpoint_url, json.dumps(json_request))
    print(json.loads(request.content))

def set_shoot(mode):
    endpoint_url = api_service_urls['camera'] + '/camera'
    json_request = {
         "method": "setShootMode",
         "params": [mode],
         "id": 1,
         "version": "1.0"
        }
    request = requests.post(endpoint_url, json.dumps(json_request))
    print(json.loads(request.content))
def get_shoot_mode():
    endpoint_url = api_service_urls['camera'] + '/camera'
    json_request = {
         "method": "getShootMode",
         "params": [],
         "id": 1,
         "version": "1.0"
        }
    request = requests.post(endpoint_url, json.dumps(json_request))
    print(json.loads(request.content))

def take_a_pic():
    endpoint_url = api_service_urls['camera'] + '/camera'
    json_request = {
        "method" : "actTakePicture",
        "params" : [],
        "id" : 1,
        "version" : api_version
    }
    request = requests.post(endpoint_url, json.dumps(json_request))
    print(json.loads(request.content))
start_rec()
set_remote()
set_shoot('still')
get_shoot_mode()
take_a_pic()
