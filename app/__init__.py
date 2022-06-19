from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://calebporto:2299346271@localhost/estefanygama'  # Definindo a conexão do SQLAlchemy com o banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'  # Desativando recurso do SQLAlchemy que gasta muita memória e não é utilizado
app.config['SECRET_KEY'] = '2299346271'  # Secret key para criptografar cookies
app.config['USE_SESSION_FOR_NEXT'] = 'True'  # Excluindo a variável 'next' da string de recirecionamento do login_required

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app\static\media')  # Definindo pasta de destino dos uploads das imagens

login_manager = LoginManager(app)
login_manager.login_view = "/login"  # Definindo a página de redirecionamento caso o usuário não esteja logado através de login_required
db = SQLAlchemy(app)


from app.routes import client, admin