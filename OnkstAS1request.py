import time
class Request:

    def getRequest(self, host, path, query) -> bytearray:
        self.request = bytearray()
        self.request += b'GET ' + path.encode() + query.encode() + b' HTTP/1.0' + b'\nHost: ' + host.encode() + b'\nConnection: close\n\n'
        return self.request

    def headRequest(self, host) -> bytearray:
        self.request = bytearray()
        self.request += b'HEAD /robots.txt HTTP/1.0\n' + b'Host: ' + host.encode() + b'\nConnection: close\n\n'
        return self.request