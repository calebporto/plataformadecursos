from app import app, db
from flask import render_template, request, redirect, url_for
from app.models.tables import User
from flask_login import current_user, login_required, login_user, logout_user


message = [{"message": "A entrada de usuário viola nossos padrões de segurança", "error":True},  # Mensagem para possível SQL Injection
            {"message": "Login ou senha não conferem.", "error": True},  # Mensagem para login ou senha inválidos
            {"message": "Nome, e-mail e login devem ter entre 8 e 45 caracteres", "error": True},  # Entrada inválida
            {"message": "CPF inválido", "error": True},  # CPF inválido
            {"message": "Senha inválida", "error": True},  # CPF inválido
            {"message": "Já existe um usuário com o mesmo e-mail, CPF ou login", "error": True},  # CPF inválido
            {"error": False}]  # Caso login e senha estejam ok, error será False

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Colunas do banco de dados
    definitive_keys = ['name', 'email', 'cpf', 'login', 'pwd', 'is_admin']
    
    # Dicionário com os dados verificados
    definitive = {}
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        login = request.form.get("login")
        senha = request.form.get("pwd")
        confirmation = request.form.get("confirmation")

        # Detectando SQL Injection e Validando dados do usuário
        for input in [name, email, login]:
            print (input)
            if User.sql_injection_detect(input.lower()):
                return render_template('register.html', message=message[0])
            if len(input) > 45 or len(input) < 8:
                return render_template('register.html', message=message[2])
        
        if sql_injection_detect(cpf.lower()) or not cpf.isdigit() or len(cpf) != 11:
            return render_template("register.html", message=message[3])
        
        if len(senha) < 8 or len(senha) > 20 or senha != confirmation:
            return render_template("register.html", message=message[4])
        
        definitive[definitive_keys[0]] = name.lower()
        definitive[definitive_keys[1]] = email.lower()
        definitive[definitive_keys[2]] = cpf.lower()
        definitive[definitive_keys[3]] = login.lower()
        definitive[definitive_keys[4]] = senha
        definitive[definitive_keys[5]] = False

        
        # Consultando se não existe outro usuário com o mesmo email, CPF ou login
        if User.user_exists(definitive['email'], definitive['cpf'], definitive['login']):
            return render_template("register.html", message=message[5])


        # Fazendo commit no banco de dados com os dados já tratados no dicionário 'definitive'
        user = User(definitive['name'], definitive['email'], definitive['cpf'], definitive['login'], definitive['pwd'], definitive['is_admin'])
        db.session.add(user)
        db.session.commit()
        
        return redirect("/login")
    else:
        return render_template("register.html", message=message[6])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
                
        # Requests de entradas do usuário
        login = request.form.get("login")
        pwd = request.form.get("pwd")
        # Checando nome de usuário
        if sql_injection_detect(login) == True:
            return render_template("login.html", message=message[0])
        
        # Buscando usuário pelo input fornecido, que pode ser email, cpf ou login
        user = User.query.filter((User.email == login) | (User.CPF == login) | (User.login == login)).first()

        # Caso não haja usuário cadastrado ou a senha esteja incorreta, retorna à página de login com mensagem de erro
        if not user or not user.verify_password(pwd):
            return render_template("login.html", message=message[1])

        print(user.is_admin)

        login_user(user)

        print(current_user.is_admin)

        return redirect(url_for("panel"))

    else:
        try:
            if current_user.name:
                return redirect('/panel')
        except AttributeError:
            return render_template("login.html", message=message[6])
        except:
            return 'Erro Inesperado'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/panel')
@login_required
def panel():
    print(current_user.is_admin, current_user.name)
    return render_template('panel.html')


# Função para detectar possíveis ataques de SQL Injection
def sql_injection_detect(input):
    injections = ['--', ' select ', ' insert ', ' delete ', ' drop ', ' update ', ' union ', ' create ', ' or ']
    
    for injection in injections:
        if injection in input.lower():
            return True
    return False