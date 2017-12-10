# HPDF week-1 tasks

from flask import Flask,render_template,request,make_response,abort
from urllib.request import urlopen
import json


app = Flask(__name__)

class Author:
	def __init__(self,name,id):
		self.name = name
		self.id = id
		self.pCount = 0

@app.route('/')                                                     #task1 - hello world
def greet():
    return "Hello World - Vinitha shree"
	
@app.route('/authors')                                              #task2 - displaying authors and their post count from json
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


@app.route("/set")                                                  #task3 - setting cookie
def settcookie():
    resp=make_response('setting cookie!')
    resp.set_cookie('name','vinitha')
    resp.set_cookie('age','20')
    return resp


@app.route("/get")                                                  #task4 - retreiving cookie
def getcookie():
    cookie1=request.cookies.get('name')
    cookie2=request.cookies.get('age')
    x= ("name - %s  & age - %s ") %(cookie1,cookie2)
    
    return x

@app.route("/robot.txt")                                            #task5 - denying request to robot.txt page
def deny():
        abort(403)

 
@app.route("/html")                                                 #task6 - rendering html file
def pro():
        return render_template("college.html")

@app.route("/form")                                                 #task7 - fething user input and displaying
def form():
        return render_template("form.html")


@app.route('/send' ,  methods=['POST','GET'])
def send():
        if  request.method ==  'POST':
                name=request.form['name']
                return render_template('name.html' , name=name)
        
        return  "no name"

if __name__=='__main__':
	app.run(debug=True, port=8080)

