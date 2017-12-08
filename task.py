
from flask import Flask,render_template,request,make_response,abort
from urllib.request import urlopen
import json
import logging

logging.basicConfig(filename='nam.log',level=logging.INFO  , format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

class Author:
	def __init__(self,name,id):
		self.name = name
		self.id = id
		self.pCount = 0

@app.route('/')
def greet():
    return "Hello World - Vinitha shree"
	
@app.route('/authors')
def fetchAndDisplay():
	urlAuthors = "https://jsonplaceholder.typicode.com/users"
	urlPosts = "https://jsonplaceholder.typicode.com/posts"
	
	print('Downloading authors')
	with urlopen(urlAuthors) as conn:
		aList = json.loads(conn.read().decode())
	print('Downloading posts')
	with urlopen(urlPosts) as conn:
		pList = json.loads(conn.read().decode())
			
	#authors = [Author(aList[i]["name"],aList[i]["id"]) for i in range(len(aList))]
	print('Setting up authors')
	authors = []
	for i in range(len(aList)):
		authors.append(Author(aList[i]["name"],aList[i]["id"]))
	
	print("Starting Post count loop")
	for author in authors:
		for post in pList:
			if post["userId"] == author.id:
				author.pCount = author.pCount + 1
		
	return render_template("authors.html",authors=authors)


@app.route("/set")
def settcookie():
    resp=make_response('setting cookie!')
    resp.set_cookie('name','vinitha')
    resp.set_cookie('age','20')
    return resp


@app.route("/get")
def getcookie():
    cookie1=request.cookies.get('name')
    cookie2=request.cookies.get('age')
    x= ("name - %s  & age - %s ") %(cookie1,cookie2)
    
    return x

@app.route("/robot.txt")
def deny():
        abort(403)

 
@app.route("/html")
def pro():
        return render_template("college.html")


@app.route('/send' ,  methods=['POST','GET'])
def send():
        if  request.method ==  'POST':
                name=request.form['name']
                logging.info("name: %s" %name)
                return render_template('name.html' , name=name)
        
        return  "no name"

if __name__=='__main__':
	app.run(debug=True, port=8080)
