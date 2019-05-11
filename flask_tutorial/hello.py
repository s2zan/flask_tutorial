from flask import Flask, send_from_directory, request, render_template
import datetime
import json
import sqlite3

def init_db(database_file):
	conn = sqlite3.connect("tuto.db")
	cur = conn.cursor()

	cur.execute("CREATE TABLE IF NOT EXISTS history ("
			+"`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
			+"`date` datetime,"
			+"`path` text,"
			+"`result` text"
			+")")

	conn.close()

def create_app():
	image_dir = "images"
	database_file = 'tuto.db'
	
	app = Flask(__name__)
	app.config["DATABASE"] = database_file
	app.config["IMAGE_DIR"] = image_dir

	@app.route('/')
	def hello_world():
		return send_from_directory(directory="", filename="index.html")


	@app.route("/upload", methods=['POST'])
	def upload():
		if 'file' not in request.files:
			save_history('No file part', '')
			return "", 400 
		f = request.files["file"]

		if f.filename == '':
			save_history('No selected file', '')
			return "", 400

		path = "images/"+f.filename

		f.save(path)
		save_history('save success', path)

		print(datetime.datetime.now())
		return json.dumps({"path": path}), 200


	def save_history(result, path):
		conn = sqlite3.connect("tuto.db")
		cur = conn.cursor()

		sql = "INSERT INTO history (path, date, result) values (?, ?, ?)"
		cur.execute(sql, (path, datetime.datetime.now(), result))

		conn.commit()
		conn.close()


	@app.route("/images/<name>")
	def image(name):
		return send_from_directory(directory="../" + app.config["IMAGE_DIR"], filename=name)


	@app.route("/history")
	def history():
		print('test')
		conn = sqlite3.connect("tuto.db")
		cur = conn.cursor()
		cur.execute("select * from history")

		rows = cur.fetchall()
		for row in rows:
			print(row)

		conn.close()
		return render_template("history.html",rows = rows)
	
	return app