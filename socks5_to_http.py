import http.server
import socketserver
import socket
import threading
import requests
import socks
from urllib.parse import urlparse

# SOCKS5 代理配置
SOCKS5_PROXY_HOST = 'localhost'
SOCKS5_PROXY_PORT = 1086

# 设置 SOCKS5 代理
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
socket.socket = socks.socksocket

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_HEAD(self):
        self.handle_request()

    def do_OPTIONS(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def do_CONNECT(self):
        self.handle_connect()

    def handle_request(self):
        parsed_url = urlparse(self.path)
        target_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        if parsed_url.query:
            target_url += f"?{parsed_url.query}"
        
        headers = {key: value for key, value in self.headers.items() if key != 'Host'}
        method = self.command

        try:
            if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
                response = requests.request(method, target_url, headers=headers, timeout=10)
            elif method in ['POST', 'PUT', 'PATCH']:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                response = requests.request(method, target_url, headers=headers, data=post_data, timeout=10)
            
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            if method != 'HEAD':
                self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, f"Error fetching {self.path}: {e}")

    def handle_connect(self):
        address = self.path.split(':')
        hostname = address[0]
        port = int(address[1])

        try:
            # 连接到目标服务器
            target_sock = socks.socksocket()
            target_sock.connect((hostname, port))
            self.send_response(200, 'Connection Established')
            self.end_headers()

            # 在客户端和目标服务器之间创建线程转发数据
            client_thread = threading.Thread(target=self.forward_data, args=(self.connection, target_sock))
            target_thread = threading.Thread(target=self.forward_data, args=(target_sock, self.connection))
            client_thread.start()
            target_thread.start()
            client_thread.join()
            target_thread.join()
        except Exception as e:
            self.send_error(500, f"CONNECT error: {e}")

    def forward_data(self, source, destination):
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)
        except Exception as e:
            pass
        finally:
            source.close()
            destination.close()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def run(server_class=ThreadingHTTPServer, handler_class=ProxyHTTPRequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http proxy on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
