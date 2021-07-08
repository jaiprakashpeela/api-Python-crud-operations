from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgres"

@app.route('/')
def main():
    return {"name": "Jai"}


if __name__ == '__main__':
    app.run(debug=True)
