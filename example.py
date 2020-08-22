from libsonyapi.camera import Camera
from libsonyapi.actions import Actions

camera = Camera()  # create camera instance
camera_info = camera.info()  # get camera camera_info
print(camera_info)

print(camera.name)  # print name of camera
print(camera.api_version)  # print api version of camera

camera.do(Actions.actTakePicture)  # take a picture

fNumber = camera.do(Actions.getFNumber)
print(fNumber)  # prints fnumber

camera.do(Actions.setFNumber, "5")  # set aperture to 5
