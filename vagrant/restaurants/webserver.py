from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import database
import cgi
import utils


class webserverHandler(BaseHTTPRequestHandler):


	def do_GET(self):
		try:
			output = ""
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<html><body>"
				output += "<h1>Restaurants</h1>"
				output +="<a href='/restaurants/new'>Add a new one!</a>"

				restaurants = database.get_restaurants()
				for restaurant in restaurants:
					output += "<p>%s</p>" % restaurant.name
					output += "<a href='/restaurants/%d/edit'>Edit</a>" % restaurant.id
					output += "<br/>"
					output += "<a href='/restaurants/%d/delete'>Delete</a>" % restaurant.id
					output += "<br/>"

				output += "</html></body>"
			elif self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<html><body>"
				output += "<h1>Make a new restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data'>"
				output += "<input type='text' name='newRestaurant'>"
				output += "<input type='submit'>"
				output += "</form>"
				output += "</html></body>"

			elif self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				id = utils.id_from_path(self.path)

				restaurant = database.get_restaurant(id)
				output += "<html><body>"
				output += "<h1>Edit the restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data'>"
				output += "<input type='text' name='newName' value='%s'>" % restaurant.name
				output += "<input type='submit'>"
				output += "</form>"
				output += "</html></body>"
			elif self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				id = utils.id_from_path(self.path)

				restaurant = database.get_restaurant(id)
				output += "<html><body>"
				output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
				output += "<form method='POST' enctype='multipart/form-data'>"
				output += "<input type='submit' value='Confirm'>"
				output += "</form>"
				output += "</html></body>"
			self.wfile.write(output)
			print output

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == "multipart/form-data":
				fields = cgi.parse_multipart(self.rfile, pdict)

			if self.path.endswith("/restaurants/new"):

				name = fields.get("newRestaurant")[0]
				database.add_restaurant(name = name)

			elif self.path.endswith("/edit"):

				name = fields.get("newName")[0]
				id = utils.id_from_path(self.path)

				database.update_restaurant(id, name)
			elif self.path.endswith("/delete"):
				id = utils.id_from_path(self.path)
				database.remove_restaurant(id)

			self.send_response(301)
			self.send_header("Location", "/restaurants")
			self.end_headers()	

		except Exception, e:
			self.send_error(500, "Something went wrong %s" % e)

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "ctrl+C entered, stopping web server..."
		server.socket.close()

if __name__ == "__main__":
	main()