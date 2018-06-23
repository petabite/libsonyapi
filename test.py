import libsonyapi
from libsonyapi import Actions

camera = libsonyapi.Camera()
camera_info = camera.info()
print(camera.do(Actions.getFNumber))
print(camera.do(Actions.startLiveview))
# set = camera.do('setFNumber', '5')
# print(set.response)
