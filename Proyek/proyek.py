from flask import Flask, render_template, session, request, abort, redirect, url_for, copy_current_request_context
import os, MySQLdb

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.static_folder = 'static'

db = MySQLdb.connect("localhost","m26415079","TOS","m26415079")
cursor = db.cursor()

@app.route("/")
@app.route("/login")
def index(status=None):
  if session.get('logged_in') == True:
    return redirect(url_for('home'))	
  session['logged_in'] = False
  return render_template("login.html",status=status)

@app.route("/cek", methods=['POST'])
def cek():
  if request.method == 'POST':
    sql = "SELECT * FROM puser WHERE username = '%s' AND password = md5('%s') " %(request.form['username'], request.form['password'])
    cursor.execute(sql)
    if (cursor.rowcount == 1):
      results = cursor.fetchone()
      session['user'] = request.form['username']
      session['nama'] = results[1]
      session['logged_in'] = True
      return redirect(url_for('home'))
    else:
      return render_template("login.html",status=1)
  else:
    return redirect(url_for('index'))

@app.route("/register", methods=['POST'])
def register():
  if request.method == 'POST':
    sql = "SELECT * FROM puser WHERE username = '%s' " %(request.form['username'])
    cursor.execute(sql)
    if (cursor.rowcount > 0):
      return render_template("login.html",status=2)
    else:
      sql = "INSERT INTO puser VALUES(NULL, '%s', '%s', 0, '%s', md5('%s'))" %(request.form['name'], request.form['email'], request.form['username'], request.form['password'])
      cursor.execute(sql)
      db.commit()
      return redirect(url_for('home'))

@app.route("/home", methods=['GET'])
def home(tabelBCA=None, tabelBNI=None, tabelCIMB=None, tabelMan=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  if request.method == 'GET':
    sql = "SELECT * FROM kursbca order by id desc LIMIT 1"
    cursor.execute(sql)
    data1=cursor.fetchall()

    sql = "SELECT * FROM kursbni order by id desc LIMIT 1"
    cursor.execute(sql)
    data2=cursor.fetchall()
    
    sql = "SELECT * FROM kurscimb order by id desc LIMIT 1"
    cursor.execute(sql)
    data3=cursor.fetchall()
    
    sql = "SELECT * FROM kursman order by id desc LIMIT 1"
    cursor.execute(sql)
    data4=cursor.fetchall()
    return render_template("index.html", tabelBCA=data1, tabelBNI=data2, tabelCIMB=data3, tabelMan=data4)

@app.route("/logout")
def dropsession():
  session.pop('user', None)
  session.pop('nama', None)
  session['logged_in'] = False
  return redirect(url_for('index'))

@app.route("/bca")
def bca(tabel=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  sql = "SELECT * FROM kursbca order by id desc LIMIT 5"
  cursor.execute(sql)
  data=cursor.fetchall()
  return render_template("bca.html",tabel=data)

@app.route("/man")
def man(tabel=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  sql = "SELECT * FROM kursman order by id desc LIMIT 5"
  cursor.execute(sql)
  data=cursor.fetchall()
  return render_template("mandiri.html",tabel=data)

@app.route("/cimb")
def cimb(tabel=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  sql = "SELECT * FROM kurscimb order by id desc LIMIT 5"
  cursor.execute(sql)
  data=cursor.fetchall()
  return render_template("cimb.html",tabel=data)

@app.route("/bni")
def bni(tabel=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  sql = "SELECT * FROM kursbni order by id desc LIMIT 5"
  cursor.execute(sql)
  data=cursor.fetchall()
  return render_template("bni.html",tabel=data)

@app.route("/profile")
def profile(tabel=None):
  if session.get('logged_in') == False:
  	return redirect(url_for('index'))
  sql = "SELECT * FROM puser WHERE username = '%s'" %(session.get('user'))
  cursor.execute(sql)
  data=cursor.fetchall()
  return render_template("profile.html",tabel=data)

@app.route("/update", methods=['POST'])
def update():
  if request.method == 'POST':
    sql = "update puser set nama='%s', email='%s', notif='%s', password=md5('%s') WHERE username = '%s' " %(request.form['nama'],request.form['email'],request.form['notif'],request.form['password'],request.form['username'])
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=15079, debug=True)
