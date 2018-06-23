import socket
import requests
import json
import xml.etree.ElementTree as ET

class Camera(object):
    def __init__(self):
        self.xml_url = self.discover()
        self.name, self.api_version, self.services = self.connect(self.xml_url)
        self.camera_endpoint_url = self.services['camera'] + '/camera'
        self.available_apis = self.do("getAvailableApiList")['result']
        # prepare camera for rec mode
        if 'startRecMode' in self.available_apis[0]:
            self.do('startRecMode')
        self.available_apis = self.do("getAvailableApiList")['result']

    def discover(self):
        """
        discover camera using upnp ssdp method, return url for device xml
        """
        msg = (
            'M-SEARCH * HTTP/1.1\r\n'
            'HOST: 239.255.255.250:1900\r\n'
            'MAN: \"ssdp:discover\" \r\n'
            'MX: 2\r\n'
            'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n'
            '\r\n').encode()
        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(2)
        s.sendto(msg, ('239.255.255.250', 1900))
        try:
            while True:
                data, addr = s.recvfrom(65507)
                decoded_data = data.decode()
                # get xml url from ssdp response
                for item in decoded_data.split('\n'):
                    if 'LOCATION' in item:
                        return item.strip().split(' ')[1]  # get location url from ssdp response
        except socket.timeout:
            raise ConnectionError('you are not connected to the camera\'s wifi')

    def connect(self, xml_url):
        """
        returns name, api_version, api_service_urls on success
        """
        device_xml_request = requests.get(xml_url)
        xml_file = str(device_xml_request.content.decode())
        xml = ET.fromstring(xml_file)
        name = xml.find('{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}friendlyName').text
        api_version = xml.find('{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo/{urn:schemas-sony-com:av}X_ScalarWebAPI_Version').text
        service_list = xml.find('{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo/{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceList')
        # print(self.api_version)
        api_service_urls = {}
        for service in service_list:
            service_type = service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType').text
            action_url = service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ActionList_URL').text
            api_service_urls[service_type] = action_url
        # print(self.api_service_urls)
        return name, api_version, api_service_urls

    def info(self):
        return {
            'name' : self.name,
            'api version' : self.api_version,
            'supported services' : list(self.services.keys()),
            'available apis' : self.available_apis
        }
    def post_request(self, url, method, param = [] ):
        """
        sends post request to url with method and param as json
        """
        if type(param) is not list:
            param = [param]
        json_request = {
             "method": method,
             "params": param,
             "id": 1,
             "version": "1.0"
            }
        request = requests.post(url, json.dumps(json_request))
        response = json.loads(request.content)
        # print(response)
        if 'error' in list(response.keys()):
            print('Error: ')
            print(response)
        else:
            return response
    # TODO: response handler, return result of do, etc
    # the following functions make call to sony camera api
    def do(self, method, param=[]):
        """
        this calls to camera service api, require method and param arg
        """
        response = self.post_request(self.camera_endpoint_url, method, param)
        return response

class ConnectionError(Exception):
    pass

class Actions(object):
    """
    contains string literals for all
    the function in sony camera api
    """
    setShootMode = 'setShootMode'
    getShootMode = 'getShootMode'
    getSupportedShootMode = 'getSupportedShootMode'
    getAvailableShootMode = 'getAvailableShootMode'
    actTakePicture = 'actTakePicture'
    awaitTakePicture = 'awaitTakePicture'
    startContShooting = 'startContShooting'
    stopContShooting = 'stopContShooting'
    startMovieRec = 'startMovieRec'
    stopMovieRec = 'stopMovieRec'
    startAudioRec = 'startAudioRec'
    stopAudioRec = 'stopAudioRec'
    startIntervalStillRec = 'startIntervalStillRec'
    stopIntervalStillRec = 'stopIntervalStillRec'
    startLoopRec = 'startLoopRec'
    stopLoopRec = 'stopLoopRec'
    startLiveview = 'startLiveview'
    stopLiveview = 'stopLiveview'
    startLiveviewWithSize = 'startLiveviewWithSize'
    getLiveviewSize = 'getLiveviewSize'
    getSupportedLiveviewSize = 'getSupportedLiveviewSize'
    getAvailableLiveviewSize = 'getAvailableLiveviewSize'
    setLiveviewFrameInfo = 'setLiveviewFrameInfo'
    getLiveviewFrameInfo = 'getLiveviewFrameInfo'
    actZoom = 'actZoom'
    setZoomSetting = 'setZoomSetting'
    getZoomSetting = 'getZoomSetting'
    getSupportedZoomSetting = 'getSupportedZoomSetting'
    getAvailableZoomSetting = 'getAvailableZoomSetting'
    actHalfPressShutter = 'actHalfPressShutter'
    cancelHalfPressShutter = 'cancelHalfPressShutter'
    setTouchAFPosition = 'setTouchAFPosition'
    getTouchAFPosition = 'getTouchAFPosition'
    cancelTouchAFPosition = 'cancelTouchAFPosition'
    actTrackingFocus = 'actTrackingFocus'
    cancelTrackingFocus = 'cancelTrackingFocus'
    setTrackingFocus = 'setTrackingFocus'
    getTrackingFocus = 'getTrackingFocus'
    getSupportedTrackingFocus = 'getSupportedTrackingFocus'
    getAvailableTrackingFocus = 'getAvailableTrackingFocus'
    setContShootingMode = 'setContShootingMode'
    getContShootingMode = 'getContShootingMode'
    getSupportedContShootingMode = 'getSupportedContShootingMode'
    getAvailableContShootingMode = 'getAvailableContShootingMode'
    setContShootingSpeed = 'setContShootingSpeed'
    getContShootingSpeed = 'getContShootingSpeed'
    getSupportedContShootingSpeed = 'getSupportedContShootingSpeed'
    getAvailableContShootingSpeed = 'getAvailableContShootingSpeed'
    setSelfTimer = 'setSelfTimer'
    getSelfTimer = 'getSelfTimer'
    getSupportedSelfTimer = 'getSupportedSelfTimer'
    getAvailableSelfTimer = 'getAvailableSelfTimer'
    setExposureMode = 'setExposureMode'
    getExposureMode = 'getExposureMode'
    getSupportedExposureMode = 'getSupportedExposureMode'
    getAvailableExposureMode = 'getAvailableExposureMode'
    setFocusMode = 'setFocusMode'
    getFocusMode = 'getFocusMode'
    getSupportedFocusMode = 'getSupportedFocusMode'
    getAvailableFocusMode = 'getAvailableFocusMode'
    setExposureCompensation = 'setExposureCompensation'
    getExposureCompensation = 'getExposureCompensation'
    getSupportedExposureCompensation = 'getSupportedExposureCompensation'
    getAvailableExposureCompensation = 'getAvailableExposureCompensation'
    setFNumber = 'setFNumber'
    getFNumber = 'getFNumber'
    getSupportedFNumber = 'getSupportedFNumber'
    getAvailableFNumber = 'getAvailableFNumber'
    setShutterSpeed = 'setShutterSpeed'
    getShutterSpeed = 'getShutterSpeed'
    getSupportedShutterSpeed = 'getSupportedShutterSpeed'
    getAvailableShutterSpeed = 'getAvailableShutterSpeed'
    setIsoSpeedRate = 'setIsoSpeedRate'
    getIsoSpeedRate = 'getIsoSpeedRate'
    getSupportedIsoSpeedRate = 'getSupportedIsoSpeedRate'
    getAvailableIsoSpeedRate = 'getAvailableIsoSpeedRate'
    setWhiteBalance = 'setWhiteBalance'
    getWhiteBalance = 'getWhiteBalance'
    getSupportedWhiteBalance = 'getSupportedWhiteBalance'
    getAvailableWhiteBalance = 'getAvailableWhiteBalance'
    actWhiteBalanceOnePushCustom = 'actWhiteBalanceOnePushCustom'
    setProgramShift = 'setProgramShift'
    getSupportedProgramShift = 'getSupportedProgramShift'
    setFlashMode = 'setFlashMode'
    getFlashMode = 'getFlashMode'
    getSupportedFlashMode = 'getSupportedFlashMode'
    getAvailableFlashMode = 'getAvailableFlashMode'
    setStillSize = 'setStillSize'
    getStillSize = 'getStillSize'
    getSupportedStillSize = 'getSupportedStillSize'
    getAvailableStillSize = 'getAvailableStillSize'
    setStillQuality = 'setStillQuality'
    getStillQuality = 'getStillQuality'
    getSupportedStillQuality = 'getSupportedStillQuality'
    getAvailableStillQuality = 'getAvailableStillQuality'
    setPostviewImageSize = 'setPostviewImageSize'
    getPostviewImageSize = 'getPostviewImageSize'
    getSupportedPostviewImageSize = 'getSupportedPostviewImageSize'
    getAvailablePostviewImageSize = 'getAvailablePostviewImageSize'
    setMovieFileFormat = 'setMovieFileFormat'
    getMovieFileFormat = 'getMovieFileFormat'
    getSupportedMovieFileFormat = 'getSupportedMovieFileFormat'
    getAvailableMovieFileFormat = 'getAvailableMovieFileFormat'
    setMovieQuality = 'setMovieQuality'
    getMovieQuality = 'getMovieQuality'
    getSupportedMovieQuality = 'getSupportedMovieQuality'
    getAvailableMovieQuality = 'getAvailableMovieQuality'
    setSteadyMode = 'setSteadyMode'
    getSteadyMode = 'getSteadyMode'
    getSupportedSteadyMode = 'getSupportedSteadyMode'
    getAvailableSteadyMode = 'getAvailableSteadyMode'
    setViewAngle = 'setViewAngle'
    getViewAngle = 'getViewAngle'
    getSupportedViewAngle = 'getSupportedViewAngle'
    getAvailableViewAngle = 'getAvailableViewAngle'
    setSceneSelection = 'setSceneSelection'
    getSceneSelection = 'getSceneSelection'
    getSupportedSceneSelection = 'getSupportedSceneSelection'
    getAvailableSceneSelection = 'getAvailableSceneSelection'
    setColorSetting = 'setColorSetting'
    getColorSetting = 'getColorSetting'
    getSupportedColorSetting = 'getSupportedColorSetting'
    getAvailableColorSetting = 'getAvailableColorSetting'
    setIntervalTime = 'setIntervalTime'
    getIntervalTime = 'getIntervalTime'
    getSupportedIntervalTime = 'getSupportedIntervalTime'
    getAvailableIntervalTime = 'getAvailableIntervalTime'
    setLoopRecTime = 'setLoopRecTime'
    getLoopRecTime = 'getLoopRecTime'
    getSupportedLoopRecTime = 'getSupportedLoopRecTime'
    getAvailableLoopRecTime = 'getAvailableLoopRecTime'
    setWindNoiseReduction = 'setWindNoiseReduction'
    getWindNoiseReduction = 'getWindNoiseReduction'
    getSupportedWindNoiseReduction = 'getSupportedWindNoiseReduction'
    getAvailableWindNoiseReduction = 'getAvailableWindNoiseReduction'
    setAudioRecording = 'setAudioRecording'
    getAudioRecording = 'getAudioRecording'
    getSupportedAudioRecording = 'getSupportedAudioRecording'
    getAvailableAudioRecording = 'getAvailableAudioRecording'
    setFlipSetting = 'setFlipSetting'
    getFlipSetting = 'getFlipSetting'
    getSupportedFlipSetting = 'getSupportedFlipSetting'
    getAvailableFlipSetting = 'getAvailableFlipSetting'
    setTvColorSystem = 'setTvColorSystem'
    getTvColorSystem = 'getTvColorSystem'
    getSupportedTvColorSystem = 'getSupportedTvColorSystem'
    getAvailableTvColorSystem = 'getAvailableTvColorSystem'
    startRecMode = 'startRecMode'
    stopRecMo = 'stopRecMo'
