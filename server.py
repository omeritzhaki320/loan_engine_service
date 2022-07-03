import local_secrets
import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import routes

# CONSTANTS
HOST = local_secrets.host
USER = local_secrets.user
PASSWD = local_secrets.passwd
DATABASE = local_secrets.database

app = Flask(__name__)
app.register_blueprint(routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USER + ':' + PASSWD + '@' + HOST + '/' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    models.db.create_all()
    app.run(debug=True)
