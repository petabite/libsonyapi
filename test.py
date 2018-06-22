import libsonyapi
from libsonyapi_functions import *

camera = libsonyapi.Camera()
camera_info = camera.info()
print(camera.do('getFNumber'))
set = camera.set('setFNumber', '5')
print(set.response)
