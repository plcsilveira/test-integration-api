from app.database import db
from sqlalchemy.orm import relationship

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False, unique=True)
    endereco = db.Column(db.String(150), nullable=False)
    fretes = relationship("Frete", backref="cliente", lazy=True)