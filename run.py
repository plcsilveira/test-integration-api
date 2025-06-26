from app import create_app, db

app = create_app()

# Cria as tabelas do banco de dados se não existirem
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)