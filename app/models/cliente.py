from app.database import db
from sqlalchemy.orm import relationship

class Cliente(db.Model):
    codigo_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    endereco = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False, unique=True)
    fretes = relationship("Frete", backref="cliente", lazy=True)