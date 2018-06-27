import libsonyapi
from libsonyapi import Actions
import requests

camera = libsonyapi.Camera() # create camera instance
camera_info = camera.info() # get camera camera_info
print(camera_info)

print(camera.name) # print name of camera
print(camera.api_version) # print api version of camera

camera.do(Actions.actTakePicture) # take a picture

fNumber = camera.do(Actions.getFNumber)
print(fNumber) # prints response from camera, which includes f-number

camera.do(Actions.setFNumber, '5') # set fnumber to 5
