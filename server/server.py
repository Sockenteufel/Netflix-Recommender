#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import ssl
import sys
from recommender import listFilms

PORT_NUMBER = 443

def resultToHtml(results):
	resHtml = """
		<table class="tg" style="undefined;table-layout: fixed; width: 653px">
		<colgroup>
		<col style="width: 96px">
		<col style="width: 316px">
		<col style="width: 158px">
		<col style="width: 83px">
		</colgroup>
		  <tr>
		    <th class="tg-8ypj">Id</th>
		    <th class="tg-8ypj">Title</th>
		    <th class="tg-rt4i">Score</th>
		    <th class="tg-8ypj">Year</th>
		  </tr>
	"""

	for i in range(0,len(results),4):
		resHtml += "<tr><td class='tg-g145'>" + str(results[i]) + "</td><td class='tg-g145' >" +\
			str(results[i+1])+ "</td><td class='tg-g145'>" + str(results[i+3]) + "</td><td class='tg-g145'>" +\
			str(results[i+2]) + "</td></tr>"
	return resHtml + "</table>"


class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".txt"):
				mimetype='text/plain'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/recommender":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "The film is: %s" % form["id_film"].value
			self.send_response(200)
			self.end_headers()
			films = resultToHtml(listFilms(5, form["id_film"].value))
			self.wfile.write(films)

			return			
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	server.socket = ssl.wrap_socket(server.socket, keyfile='/etc/letsencrypt/live/aldelsa.northeurope.cloudapp.azure.com/privkey.pem' ,certfile='/etc/letsencrypt/live/aldelsa.northeurope.cloudapp.azure.com/cert.pem',server_side=True)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
