import flask
import sqlite3

app = flask.Flask(__name__)

@app.route('/data')
def data():
    conn = sqlite3.connect('../database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM intrusion")
    data = c.fetchall()
    formatted = []
    for row in data:
        formatted.append({
            'id': row[0],
            'time': row[1]
        })
    return flask.jsonify(formatted)

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)