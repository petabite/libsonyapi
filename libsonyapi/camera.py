import socket
import requests
import json
import xml.etree.ElementTree as ET


class Camera(object):
    def __init__(self):
        """
        create camera object
        """
        self.xml_url = self.discover()
        self.name, self.api_version, self.services = self.connect(self.xml_url)
        self.camera_endpoint_url = self.services["camera"] + "/camera"
        self.available_apis = self.do("getAvailableApiList")["result"]
        # prepare camera for rec mode
        if "startRecMode" in self.available_apis[0]:
            self.do("startRecMode")
        self.available_apis = self.do("getAvailableApiList")["result"]
        self.connected = False

    def discover(self):
        """
        discover camera using upnp ssdp method, return url for device xml
        """
        msg = (
            "M-SEARCH * HTTP/1.1\r\n"
            "HOST: 239.255.255.250:1900\r\n"
            'MAN: "ssdp:discover" \r\n'
            "MX: 2\r\n"
            "ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n"
            "\r\n"
        ).encode()
        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(2)
        s.sendto(msg, ("239.255.255.250", 1900))
        try:
            while True:
                data, addr = s.recvfrom(65507)
                decoded_data = data.decode()
                # get xml url from ssdp response
                for item in decoded_data.split("\n"):
                    if "LOCATION" in item:
                        return item.strip().split(" ")[
                            1
                        ]  # get location url from ssdp response
            self.connected = True
        except socket.timeout:
            raise ConnectionError("you are not connected to the camera's wifi")

    def connect(self, xml_url):
        """
        returns name, api_version, api_service_urls on success
        """
        device_xml_request = requests.get(xml_url)
        xml_file = str(device_xml_request.content.decode())
        xml = ET.fromstring(xml_file)
        name = xml.find(
            "{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}friendlyName"
        ).text
        api_version = xml.find(
            "{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo/{urn:schemas-sony-com:av}X_ScalarWebAPI_Version"
        ).text
        service_list = xml.find(
            "{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo/{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceList"
        )
        api_service_urls = {}
        for service in service_list:
            service_type = service.find(
                "{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType"
            ).text
            action_url = service.find(
                "{urn:schemas-sony-com:av}X_ScalarWebAPI_ActionList_URL"
            ).text
            api_service_urls[service_type] = action_url
        return name, api_version, api_service_urls

    def info(self):
        """
        returns camera info(name, api version, supported services, available apis) in a dictionary
        """
        return {
            "name": self.name,
            "api version": self.api_version,
            "supported services": list(self.services.keys()),
            "available apis": self.available_apis,
        }

    def post_request(self, url, method, param=[]):
        """
        sends post request to url with method and param as json
        """
        if type(param) is not list:
            param = [param]
        json_request = {"method": method, "params": param, "id": 1, "version": "1.0"}
        request = requests.post(url, json.dumps(json_request))
        response = json.loads(request.content)
        if "error" in list(response.keys()):
            print("Error: ")
            print(response)
        else:
            return response

    def do(self, method, param=[]):
        """
        this calls to camera service api, require method and param args
        """
        # TODO: response handler, return result of do, etc
        response = self.post_request(self.camera_endpoint_url, method, param)
        return response


class ConnectionError(Exception):
    pass
