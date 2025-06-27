from app.database import db
from sqlalchemy.orm import relationship

class Cidade(db.Model):
    codigo_cidade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    UF = db.Column(db.String(30), nullable=False)
    taxa = db.Column(db.Float(4), nullable=False)
    fretes = relationship("Frete", backref="cidade", lazy=True)