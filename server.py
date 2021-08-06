import http.server
import cgi
import base64
import requests
from requests.auth import HTTPBasicAuth

from urllib.parse import urlparse, parse_qs

class CustomServerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        key = self.server.get_auth_key()

        # Only extract the encode byte string
        auth_bytestring = base64.b64decode(self.headers.get('Authorization').split()[1])
        auth = auth_bytestring.decode('utf-8')
        auth = auth.split(':')

        response = requests.get('http://192.168.0.26/snapshot.cgi',
            auth = HTTPBasicAuth(auth[0], auth[1]))

        if response.status_code == 200:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(response.content)
        else:
            self.send_response(401)
            self.send_header(
                'WWW-Authenticate', 'Basic realm="Demo Realm"')
            self.end_headers()

    def _parse_GET(self):
        getvars = parse_qs(urlparse(self.path).query)

        return getvars

class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key

if __name__ == '__main__':
    server = CustomHTTPServer(('', 8888))
    server.set_auth('', '')
    server.serve_forever()
