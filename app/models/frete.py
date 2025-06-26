from app.database import db

class Frete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False)
