from main import db, app

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    password = db.Column(db.String(50))


with app.app_context():
    db.create_all()

