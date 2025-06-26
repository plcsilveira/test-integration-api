from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    codigo_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    # ... resto dos atributos e classes