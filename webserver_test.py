from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Catalog, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/delete"):
                catalogIDPath = self.path.split("/")[2]

                myCatalogQuery = session.query(Catalog).filter_by(
                    id=catalogIDPath).one()
                if myCatalogQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    message = ""
                    message += "<html><body>"
                    message += "<h1>Are you sure you want to delete %s?" % myCatalogQuery.name
                    message += "<form method='POST' enctype = 'multipart/form-data' action = '/catalogs/%s/delete'>" % catalogIDPath
                    message += "<input type = 'submit' value = 'Delete'>"
                    message += "</form>"
                    message += "</body></html>"
                    self.wfile.write(message)
                    return

        if self.path.endswith("/edit"):
                catalogIDPath = self.path.split("/")[2]
                myCatalogQuery = session.query(Catalog).filter_by(
                    id=catalogIDPath).one()
                if myCatalogQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    message = "<html><body>"
                    message += "<h1>"
                    message += myCatalogQuery.name
                    message += "</h1>"
                    message += "<form method='POST' enctype='multipart/form-data' action = '/catalogs/%s/edit' >" % catalogIDPath
                    message += "<input name = 'newCatalogName' type='text' placeholder = '%s' >" % myCatalogQuery.name
                    message += "<input type = 'submit' value = 'Rename'>"
                    message += "</form>"
                    message += "</body></html>"

                    self.wfile.write(message)
                    return

        if self.path.endswith("/catalogs/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1> Create New Catalog</h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/catalogs/new'><h2>'''
            message += '''<input name= 'newCatalogName' type='text' placeholder = 'New Catalog Name' >'''
            message += '''<input type= 'submit' value = 'Create'>'''
            message += "</body></html>"
            self.wfile.write(message)
            return



        if self.path.endswith("/catalogs"):
            catalogs = session.query(Catalog).all()
            message = ""
            message += "<a href ='/catalogs/new' >Create New Catalog </a></br></br> "
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # message = ""
            message += "<html><body>"
            for catalog in catalogs:
                message += catalog.name
                message += "</br>"
                message += "<a href ='/catalogs/%s/edit' >Edit </a> " % catalog.id
                message += "</br>"
                message += "<a href ='/catalogs/%s/delete' >Delete </a> " % catalog.id
                message += "</br>"
                message += "</br>"
                message += "</br>"
            message += "</body></html>"
            # message = ""
            # message += "<a href ='/catalogs/new' >Create New Catalog </a></br></br> "
            self.wfile.write(message)
            return


        if self.path.endswith("/catalog"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "You have reached the Catalog page!"
            message += '''<form method='POST' enctype='multipart/form-data' action='/catalog'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print (message)
            return


        if self.path.endswith("/catalog2"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "You have reached the 2nd Catalog page!      <a href = '/catalog' >Go Back To Catalog1</a>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/catalog'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print (message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                catalogIDPath = self.path.split("/")[2]
                myCatalogQuery = session.query(Catalog).filter_by(
                    id=catalogIDPath).one()
                if myCatalogQuery:
                    session.delete(myCatalogQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/catalogs')
                    self.end_headers()



            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCatalogName')
                    catalogIDPath = self.path.split("/")[2]

                    myCatalogQuery = session.query(Catalog).filter_by(
                        id=catalogIDPath).one()
                    if myCatalogQuery != []:
                        myCatalogQuery.name = messagecontent[0]
                        session.add(myCatalogQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/catalogs')
                        self.end_headers()


            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            if self.path.endswith("/catalogs/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCatalogName')

                newCatalog = Catalog(name = messagecontent[0])
                session.add(newCatalog)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/catalogs')
                self.end_headers()

            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]
            # output += '''<form method='POST' enctype='multipart/form-data' action='/catalog'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" Control-C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
