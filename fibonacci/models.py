from extensions.sqlalchemy import db


class Fibonacci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordinal = db.Column(db.Integer, nullable=False, unique=True)
    nth = db.Column(db.Integer, nullable=False)
