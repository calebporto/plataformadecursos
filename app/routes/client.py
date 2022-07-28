from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, request, redirect, session, url_for
from app.models.tables import Course_per_client, User, Course
from app import app, db


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
            if len(input) > 45 or len(input) < 8:
                return render_template('register.html', message=message[2])
        
        if not cpf.isdigit() or len(cpf) != 11:
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
        
        # Buscando usuário pelo input fornecido, que pode ser email, cpf ou login
        user = User.query.filter((User.email == login) | (User.CPF == login) | (User.login == login)).first()

        # Caso não haja usuário cadastrado ou a senha esteja incorreta, retorna à página de login com mensagem de erro
        if not user or not user.verify_password(pwd):
            return render_template("login.html", message=message[1])

        login_user(user, remember=True)

        if 'next' in session:
            next = session['next']

            if next is not None:
                return redirect(next)

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


@app.route('/painel')
@login_required
def panel():
    username = (current_user.name).split()[0].title()  # obtendo apenas o primeiro nome e colocando a primeira letra em maiúsculo
    client_courses =  Course.query.join(Course_per_client).filter(Course_per_client.user_id == current_user.id).all()

    return render_template('painel.html', username=username, client_courses=client_courses)

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')