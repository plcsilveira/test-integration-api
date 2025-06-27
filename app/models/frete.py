from app.database import db

class Frete(db.Model):
    codigo_frete = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30), nullable=False)
    peso = db.Column(db.Float(4), nullable=False)
    valor = db.Column(db.Float(4), nullable=False)
    codigo_cliente = db.Column(db.Integer, db.ForeignKey('cliente.codigo_cliente'), nullable=False)
    codigo_cidade = db.Column(db.Integer, db.ForeignKey('cidade.codigo_cidade'), nullable=False)
