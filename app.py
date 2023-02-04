from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import db_models
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/Loans'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

if __name__ == '__main__':
    db_models.db.create_all()
    app.run(debug=True)
