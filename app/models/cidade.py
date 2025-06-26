from app.database import db
from sqlalchemy.orm import relationship

class Cidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    taxa_entrega = db.Column(db.Float, nullable=False)
    fretes = relationship("Frete", backref="cidade", lazy=True)