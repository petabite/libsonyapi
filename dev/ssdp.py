import socket

def discover():
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
    s.sendto(msg, ('239.255.255.250', 1900) )

    try:
        while True:
            data, addr = s.recvfrom(65507)
            return data.decode()
    except socket.timeout:
        pass
