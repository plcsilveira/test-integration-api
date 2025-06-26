from flask_sqlalchemy import SQLAlchemy

# Cria uma instância do SQLAlchemy que será ligada à aplicação Flask posteriormente.
db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes' # Boa prática definir o nome da tabela
    codigo_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    endereco = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False, unique=True)
    
    # Define o relacionamento: um cliente pode ter vários fretes.
    fretes = db.relationship('Frete', backref='cliente', lazy=True)

class Cidade(db.Model):
    __tablename__ = 'cidades'
    codigo_cidade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    uf = db.Column(db.String(30), nullable=False)
    taxa = db.Column(db.Float, nullable=False)
    
    # Define o relacionamento: uma cidade pode estar em vários fretes.
    fretes = db.relationship('Frete', backref='cidade', lazy=True)

class Frete(db.Model):
    __tablename__ = 'fretes'
    codigo_frete = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    
    # Define as chaves estrangeiras (FK)
    codigo_cliente = db.Column(db.Integer, db.ForeignKey('clientes.codigo_cliente'), nullable=False)
    codigo_cidade = db.Column(db.Integer, db.ForeignKey('cidades.codigo_cidade'), nullable=False)