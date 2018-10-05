from flask import Flask, render_template, request
import sqlite3 as sql
from random import * 
import time
import math
app = Flask(__name__)
import sqlite3
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
conn = sqlite3.connect('test.db')
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/showbwdate')
def showdate():
	range1 = request.args.get("range")
	date1 = time.mktime(time.strptime(request.args.get("start"), '%Y-%m-%d'))
	date2 = time.mktime(time.strptime(request.args.get("end"), '%Y-%m-%d'))
	con = sql.connect("test.db")
	cur = con.cursor()
	start_time = time.time()
	for i in range(int(range1)): 
		ptime = date1 + random() * (date2 - date1)
		x= time.strftime('%Y-%m-%d', time.localtime(ptime))
		cur.execute("select * from allmonth where (substr(TIME,1,10)= %s)"%(x))

	end_time1 = time.time()-start_time

	start_time = time.time()
	for i in range(int(range1)): 
		ptime = date1 + random() * (date2 - date1)
		x= time.strftime('%Y-%m-%d', time.localtime(ptime))
		x = time.strptime(x, '%Y-%m-%d')
		if r.get(x) == False:
			cur.execute("select * from allmonth where (substr(TIME,1,10) =%s)"%(x))
			r.set(x,cur.fetchone())
	end_time2 = time.time()-start_time		
	cur.close()
	return render_template("list.html",rows = end_time1, timer2 = end_time2)
@app.route('/showlatlong')
def showlatlong():
	range1 = request.args.get("range")
	latitude  = request.args.get("latitude")
	longitude = request.args.get("longitude")
	km = request.args.get("km")
	con = sql.connect("test.db")
	cur = con.cursor()
	longRange = 111.320*math.cos(float(km)/110.575)
	longRange = 1/longRange	
	start_time = time.time()
	for i in range(int(range1)):
		cur.execute("select * from allmonth where (latitude between %s and %s) and (longitude between %s and %s)"%(float(latitude) - float(km)/110.575, float(latitude) + float(km)/110.575, float(longitude) - longRange, float(longitude) + longRange))
	end_time1 = time.time()-start_time

	start_time = time.time()
	for i in range(int(range1)): 
		if r.get(range1) == False:
			cur.execute("select * from allmonth where (latitude between %s and %s) and (longitude between %s and %s)"%(float(latitude) - float(km)/110.575, float(latitude) + float(km)/110.575, float(longitude) - longRange, float(longitude) + longRange))
			r.set(range1,cur.fetchall())
	end_time2 = time.time()-start_time		
	cur.close()
	return render_template("list.html",rows = end_time1, timer2 = end_time2)

@app.route('/showloc')
def showloc():
	range1 = request.args.get("range")
	location = request.args.get("location")
	con = sql.connect("test.db")
	cur = con.cursor()
	start_time = time.time()
	for i in range(int(range1)): 
		cur.execute("select * from allmonth where place LIKE %s"%('\'%'+location+'%\''))
	end_time1 = time.time()-start_time

	start_time = time.time()
	for i in range(int(range1)): 
		if r.get(location) == False:
			cur.execute("select * from allmonth where place LIKE %s"%('\'%'+location+'%\''))
			r.set(location,cur.fetchall())
	end_time2 = time.time()-start_time		
	cur.close()
	return render_template("list.html",rows = end_time1, timer2 = end_time2)

@app.route('/showmag')
def showmag():
	range1 = request.args.get("range")
	range2 = request.args.get("range1")
	range3 = request.args.get("range2")
	con = sql.connect("test.db")
	cur = con.cursor()
	start_time = time.time()
	for i in range(int(range1)): 
		cur.execute("select * from allmonth where mag=%f"%(round(uniform(float(range2), float(range3)),2)))
	end_time1 = time.time()-start_time

	start_time = time.time()
	for i in range(int(range1)): 
		randnum = round(uniform(float(range2), float(range3)),2)
		if r.get(randnum) == False:
			cur.execute("select * from allmonth where mag=%f"%(randnum))
			r.set(randnum,cur.fetchone())

	end_time2 = time.time()-start_time		
	cur.close()
	return render_template("list.html",rows = end_time1, timer2 = end_time2)

@app.route('/listall')
def list():
	range1 = request.args.get("range")
	con = sql.connect("test.db")
	cur = con.cursor()
	start_time = time.time()
	for i in range(int(range1)): 
		cur.execute("select * from allmonth where mag=%f"%(round(uniform(1.0, 10.0),2)))
	end_time1 = time.time()-start_time

	start_time = time.time()
	for i in range(int(range1)): 
		randnum = round(uniform(1.0, 10.0),2)
		if r.get(randnum) == False:		
			cur.execute("select * from allmonth where mag=%f"%(randnum))
			r.set(randnum,cur.fetchone())
	end_time2 = time.time()-start_time		
	cur.close()
	return render_template("list.html",rows = end_time1, timer2 = end_time2)

if __name__ == '__main__':
	app.run(debug="True")
