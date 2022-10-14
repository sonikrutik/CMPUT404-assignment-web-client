#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.request import urlopen

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return data.split(" ")[1]

    def get_headers(self,data):
        data = data.split("\r\n\r\n")[0]
        return data

    def get_body(self, data):
        data = data.split("\r\n\r\n")
        return data[1]

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def POST(self, url, args=None):
            code = 500
            body = ""

            if (args != None):
                args = urllib.parse.urlencode(args)
            
            urlParse = urllib.parse.urlparse(url)

            # Get the url hostname
            if urlParse.hostname:
                host = urlParse.hostname
            else:
                host = "localhost"

            # Get the url path and query
            pathQuery = urlParse.path 
            if urlParse.query != "":
                pathQuery = pathQuery + "?"
            
            pathQuery = pathQuery + urlParse.query

            # Get the url port
            port = urlParse.port
            if port == None:
                port = 80
            
            self.connect(host, port)
            message = "POST {} HTTP/1.0\r\nHost: {}\r\nContent-Length: ".format(pathQuery, host)
            if args == None:
                contentLength = "0\r\n"
            else:
                contentLength = str(len(args)) + "\r\n"

            contentType = "Content-Type: application/x-www-form-urlencoded\r\n\r\n{}\r\n".format(args)
            message = message + contentLength + contentType

            self.sendall(message)
            data = self.recvall(self.socket)
            self.socket.close()

            print(data)
            code = self.get_code(data)
            header = self.get_headers(data)
            body = self.get_body(data)
            
            return HTTPResponse(int(code), body)

    def GET(self, url, args=None):
        code = 500
        body = ""

        urlParse = urllib.parse.urlparse(url)
        parsedUrl = urlParse._replace(fragment="").geturl()
        #print("HAHAHAHAHAH", parsedUrl)

        # Get the url hostname
        if urlParse.hostname:
            host = urlParse.hostname
        else:
            host = "localhost"

        # Get the url path and query
        if urlParse.path:
            pathQuery = urlParse.path
        else: 
            pathQuery = "/"

        # Get the url port
        if urlParse.port:
            port = urlParse.port
        else:
            port = 80

        # print("HOST: ", host)
        # print("QUERY: ", pathQuery)
        # print("PORT: ", port)
        
        # Open connection
        self.connect(host, port)
        # Send data
        message = "GET {} HTTP/1.1\r\nHost: {}:{}\r\nConnection: close\r\n\r\n".format(pathQuery, host, port) 
        self.sendall(message)
        # Receive data "GET "+pathQuery+" HTTP/1.1\r\nHost: "+host+"\r\nConnection: close\r\n\r\n" 
        data = self.recvall(self.socket)
        self.socket.close()
        #print(data)

        
        code = self.get_code(data)
        header = self.get_headers(data)
        body = self.get_body(data)

        print("CODE HEHEHEHEE", code)
        print("Headers", header)
        print("BODY", body)

        
        return HTTPResponse(int(code), body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        #print(sys.argv[2], sys.argv[1])
        print("BACK FROM GET:", client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
