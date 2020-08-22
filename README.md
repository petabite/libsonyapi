# libsonyapi

Python binding for the [Sony Camera API](https://developer.sony.com/develop/cameras/)

---

# REQUIREMENTS

- a compatible Sony camera (find your camera [here](https://developer.sony.com/develop/cameras/api-information/supported-devices))
- wifi connection

# INSTALLATION

## `pip install libsonyapi`

**OR FROM SOURCE:**

1. `git clone https://github.com/petabite/libsonyapi.git` or download the [latest release](https://github.com/petabite/libsonyapi/releases)
2. `cd libsonyapi`
3. `python setup.py install`

Requires:

- [requests](https://requests.readthedocs.io/en/master/user/install/#install)

# QUICKSTART

```python
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
```

# CHANGELOG

- **v1.0 - 8/22/20**
  - first official release

# HOW IT WORKS

1. establishes connection with camera thru upnp ssdp protocol
2. make calls to camera via http post and json body
3. camera responds with json w/ info such as status and info if required by http call

# DOCS

##### Objects

- libsonyapi.Camera()
  - init a Camera object
- libsonyapi.Actions()
  - do not need to create instance
  - contains string literals of sony camera api methods for convenience (auto-complete)

##### Parameters

- **Camera.name**
  - name of the camera
- **Camera.api_version**
  - api version of camera
- **Camera.services**
  - list of services available on camera
- **Camera.available_apis**
  - list of apis currently available on camera

##### Methods

- **Camera.info(self)**
  - returns camera info(name, api_version, supported services, available api) in dict
- **Camera.do(self, method, param=[]):**
  - **METHOD:** libsony.Actions.method, where method is one listed in the API LIST below
  - **PARAM(optional):** accepts string of param if METHOD is a method that sets a value on the camera
  - Returns the json response from the camera (for debugging)
  - NOTE: your camera may not support all methods. use `Camera.do("getAvailableApiList")['result']` to get currently available APIs.
  - Refer to [Sony Camera API](https://developer.sony.com/develop/cameras/) docs for function of method and supported params

# EXAMPLES

- [**pylapse**](https://github.com/petabite/pylapse) - uses libsonyapi to automatically capture pictures for a timelapse

# API LIST

###### The table below shows the name of variables in the libsonyapi Actions class and its corresponding Sony Camera API method name

| libsonyapi Variable Name         | Sony API Method Name               |
| -------------------------------- | ---------------------------------- |
| setShootMode                     | 'setShootMode'                     |
| getShootMode                     | 'getShootMode'                     |
| getSupportedShootMode            | 'getSupportedShootMode'            |
| getAvailableShootMode            | 'getAvailableShootMode'            |
| actTakePicture                   | 'actTakePicture'                   |
| awaitTakePicture                 | 'awaitTakePicture'                 |
| startContShooting                | 'startContShooting'                |
| stopContShooting                 | 'stopContShooting'                 |
| startMovieRec                    | 'startMovieRec'                    |
| stopMovieRec                     | 'stopMovieRec'                     |
| startAudioRec                    | 'startAudioRec'                    |
| stopAudioRec                     | 'stopAudioRec'                     |
| startIntervalStillRec            | 'startIntervalStillRec'            |
| stopIntervalStillRec             | 'stopIntervalStillRec'             |
| startLoopRec                     | 'startLoopRec'                     |
| stopLoopRec                      | 'stopLoopRec'                      |
| startLiveview                    | 'startLiveview'                    |
| stopLiveview                     | 'stopLiveview'                     |
| startLiveviewWithSize            | 'startLiveviewWithSize'            |
| getLiveviewSize                  | 'getLiveviewSize'                  |
| getSupportedLiveviewSize         | 'getSupportedLiveviewSize'         |
| getAvailableLiveviewSize         | 'getAvailableLiveviewSize'         |
| setLiveviewFrameInfo             | 'setLiveviewFrameInfo'             |
| getLiveviewFrameInfo             | 'getLiveviewFrameInfo'             |
| actZoom                          | 'actZoom'                          |
| setZoomSetting                   | 'setZoomSetting'                   |
| getZoomSetting                   | 'getZoomSetting'                   |
| getSupportedZoomSetting          | 'getSupportedZoomSetting'          |
| getAvailableZoomSetting          | 'getAvailableZoomSetting'          |
| actHalfPressShutter              | 'actHalfPressShutter'              |
| cancelHalfPressShutter           | 'cancelHalfPressShutter'           |
| setTouchAFPosition               | 'setTouchAFPosition'               |
| getTouchAFPosition               | 'getTouchAFPosition'               |
| cancelTouchAFPosition            | 'cancelTouchAFPosition'            |
| actTrackingFocus                 | 'actTrackingFocus'                 |
| cancelTrackingFocus              | 'cancelTrackingFocus'              |
| setTrackingFocus                 | 'setTrackingFocus'                 |
| getTrackingFocus                 | 'getTrackingFocus'                 |
| getSupportedTrackingFocus        | 'getSupportedTrackingFocus'        |
| getAvailableTrackingFocus        | 'getAvailableTrackingFocus'        |
| setContShootingMode              | 'setContShootingMode'              |
| getContShootingMode              | 'getContShootingMode'              |
| getSupportedContShootingMode     | 'getSupportedContShootingMode'     |
| getAvailableContShootingMode     | 'getAvailableContShootingMode'     |
| setContShootingSpeed             | 'setContShootingSpeed'             |
| getContShootingSpeed             | 'getContShootingSpeed'             |
| getSupportedContShootingSpeed    | 'getSupportedContShootingSpeed'    |
| getAvailableContShootingSpeed    | 'getAvailableContShootingSpeed'    |
| setSelfTimer                     | 'setSelfTimer'                     |
| getSelfTimer                     | 'getSelfTimer'                     |
| getSupportedSelfTimer            | 'getSupportedSelfTimer'            |
| getAvailableSelfTimer            | 'getAvailableSelfTimer'            |
| setExposureMode                  | 'setExposureMode'                  |
| getExposureMode                  | 'getExposureMode'                  |
| getSupportedExposureMode         | 'getSupportedExposureMode'         |
| getAvailableExposureMode         | 'getAvailableExposureMode'         |
| setFocusMode                     | 'setFocusMode'                     |
| getFocusMode                     | 'getFocusMode'                     |
| getSupportedFocusMode            | 'getSupportedFocusMode'            |
| getAvailableFocusMode            | 'getAvailableFocusMode'            |
| setExposureCompensation          | 'setExposureCompensation'          |
| getExposureCompensation          | 'getExposureCompensation'          |
| getSupportedExposureCompensation | 'getSupportedExposureCompensation' |
| getAvailableExposureCompensation | 'getAvailableExposureCompensation' |
| setFNumber                       | 'setFNumber'                       |
| getFNumber                       | 'getFNumber'                       |
| getSupportedFNumber              | 'getSupportedFNumber'              |
| getAvailableFNumber              | 'getAvailableFNumber'              |
| setShutterSpeed                  | 'setShutterSpeed'                  |
| getShutterSpeed                  | 'getShutterSpeed'                  |
| getSupportedShutterSpeed         | 'getSupportedShutterSpeed'         |
| getAvailableShutterSpeed         | 'getAvailableShutterSpeed'         |
| setIsoSpeedRate                  | 'setIsoSpeedRate'                  |
| getIsoSpeedRate                  | 'getIsoSpeedRate'                  |
| getSupportedIsoSpeedRate         | 'getSupportedIsoSpeedRate'         |
| getAvailableIsoSpeedRate         | 'getAvailableIsoSpeedRate'         |
| setWhiteBalance                  | 'setWhiteBalance'                  |
| getWhiteBalance                  | 'getWhiteBalance'                  |
| getSupportedWhiteBalance         | 'getSupportedWhiteBalance'         |
| getAvailableWhiteBalance         | 'getAvailableWhiteBalance'         |
| actWhiteBalanceOnePushCustom     | 'actWhiteBalanceOnePushCustom'     |
| setProgramShift                  | 'setProgramShift'                  |
| getSupportedProgramShift         | 'getSupportedProgramShift'         |
| setFlashMode                     | 'setFlashMode'                     |
| getFlashMode                     | 'getFlashMode'                     |
| getSupportedFlashMode            | 'getSupportedFlashMode'            |
| getAvailableFlashMode            | 'getAvailableFlashMode'            |
| setStillSize                     | 'setStillSize'                     |
| getStillSize                     | 'getStillSize'                     |
| getSupportedStillSize            | 'getSupportedStillSize'            |
| getAvailableStillSize            | 'getAvailableStillSize'            |
| setStillQuality                  | 'setStillQuality'                  |
| getStillQuality                  | 'getStillQuality'                  |
| getSupportedStillQuality         | 'getSupportedStillQuality'         |
| getAvailableStillQuality         | 'getAvailableStillQuality'         |
| setPostviewImageSize             | 'setPostviewImageSize'             |
| getPostviewImageSize             | 'getPostviewImageSize'             |
| getSupportedPostviewImageSize    | 'getSupportedPostviewImageSize'    |
| getAvailablePostviewImageSize    | 'getAvailablePostviewImageSize'    |
| setMovieFileFormat               | 'setMovieFileFormat'               |
| getMovieFileFormat               | 'getMovieFileFormat'               |
| getSupportedMovieFileFormat      | 'getSupportedMovieFileFormat'      |
| getAvailableMovieFileFormat      | 'getAvailableMovieFileFormat'      |
| setMovieQuality                  | 'setMovieQuality'                  |
| getMovieQuality                  | 'getMovieQuality'                  |
| getSupportedMovieQuality         | 'getSupportedMovieQuality'         |
| getAvailableMovieQuality         | 'getAvailableMovieQuality'         |
| setSteadyMode                    | 'setSteadyMode'                    |
| getSteadyMode                    | 'getSteadyMode'                    |
| getSupportedSteadyMode           | 'getSupportedSteadyMode'           |
| getAvailableSteadyMode           | 'getAvailableSteadyMode'           |
| setViewAngle                     | 'setViewAngle'                     |
| getViewAngle                     | 'getViewAngle'                     |
| getSupportedViewAngle            | 'getSupportedViewAngle'            |
| getAvailableViewAngle            | 'getAvailableViewAngle'            |
| setSceneSelection                | 'setSceneSelection'                |
| getSceneSelection                | 'getSceneSelection'                |
| getSupportedSceneSelection       | 'getSupportedSceneSelection'       |
| getAvailableSceneSelection       | 'getAvailableSceneSelection'       |
| setColorSetting                  | 'setColorSetting'                  |
| getColorSetting                  | 'getColorSetting'                  |
| getSupportedColorSetting         | 'getSupportedColorSetting'         |
| getAvailableColorSetting         | 'getAvailableColorSetting'         |
| setIntervalTime                  | 'setIntervalTime'                  |
| getIntervalTime                  | 'getIntervalTime'                  |
| getSupportedIntervalTime         | 'getSupportedIntervalTime'         |
| getAvailableIntervalTime         | 'getAvailableIntervalTime'         |
| setLoopRecTime                   | 'setLoopRecTime'                   |
| getLoopRecTime                   | 'getLoopRecTime'                   |
| getSupportedLoopRecTime          | 'getSupportedLoopRecTime'          |
| getAvailableLoopRecTime          | 'getAvailableLoopRecTime'          |
| setWindNoiseReduction            | 'setWindNoiseReduction'            |
| getWindNoiseReduction            | 'getWindNoiseReduction'            |
| getSupportedWindNoiseReduction   | 'getSupportedWindNoiseReduction'   |
| getAvailableWindNoiseReduction   | 'getAvailableWindNoiseReduction'   |
| setAudioRecording                | 'setAudioRecording'                |
| getAudioRecording                | 'getAudioRecording'                |
| getSupportedAudioRecording       | 'getSupportedAudioRecording'       |
| getAvailableAudioRecording       | 'getAvailableAudioRecording'       |
| setFlipSetting                   | 'setFlipSetting'                   |
| getFlipSetting                   | 'getFlipSetting'                   |
| getSupportedFlipSetting          | 'getSupportedFlipSetting'          |
| getAvailableFlipSetting          | 'getAvailableFlipSetting'          |
| setTvColorSystem                 | 'setTvColorSystem'                 |
| getTvColorSystem                 | 'getTvColorSystem'                 |
| getSupportedTvColorSystem        | 'getSupportedTvColorSystem'        |
| getAvailableTvColorSystem        | 'getAvailableTvColorSystem'        |
| startRecMode                     | 'startRecMode'                     |
| stopRecMo                        | 'stopRecMo'                        |
