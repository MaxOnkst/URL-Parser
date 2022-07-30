from urllib.parse import urlparse

class URLparser:

    def parse(self, url):
        o = urlparse(url)

        if o.hostname is None:
            hostname = url
        else:
            hostname = o.hostname

        if o.port is None:
            port = 80
        else:
            port = o.port
        print("Parsing URL... host", hostname, ", port", port)
        return hostname, port, o.path, o.query