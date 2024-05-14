from flask import Flask
from flask import url_for

app = Flask(__name__)
 
@app.route("/")
def hello():
  return "Hello World!"

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)