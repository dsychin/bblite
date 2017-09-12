from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, parse_qs
from io import StringIO
import os
import json
import requests

class BbHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path[1:] == ''):
            html_file = open('index.html','r')
            html = html_file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            options = {'per_page': 40, 'categories': 4}
            r = requests.get('http://borneobulletin.com.bn/wp-json/wp/v2/posts', params=options)
            posts = json.load(StringIO(r.text))

            content = '<ul>'
            for post in posts:
                content += '<li><a href="/' \
                + str(post['id']) + '">' \
                + post['title']['rendered'] \
                +'</a></li>'
            content += '</ul>'

            html = html.format(content=content)
            self.wfile.write(html.encode())
        
        elif (self.path[1:] != 'favicon.ico'):
            try:
                id = int(self.path[1:])

                html_file = open('post.html','r')
                html = html_file.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                r = requests.get('http://borneobulletin.com.bn/wp-json/wp/v2/posts/' + str(id))
                post = json.load(StringIO(r.text))

                html = html.format(title=post['title']['rendered'], content=post['content']['rendered'])
                self.wfile.write(html.encode())
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write('404 Not Found!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, BbHandler)
    httpd.serve_forever()